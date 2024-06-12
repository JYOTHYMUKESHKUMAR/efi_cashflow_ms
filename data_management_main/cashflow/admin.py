from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
from decimal import Decimal, InvalidOperation
from django.contrib import messages
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django import forms

class CashInForm(forms.ModelForm):
    class Meta:
        model = CashIn
        fields = '__all__'
        
    def __init__(self, *args, **kwargs):
        super(CashInForm, self).__init__(*args, **kwargs)
        self.fields['delayed_date'].widget.attrs['style'] = 'display:none;'
        if self.instance and self.instance.status == 'Delayed':
            self.fields['delayed_date'].widget.attrs['style'] = 'display:block;'

    def clean(self):
        cleaned_data = super(CashInForm, self).clean()
        status = cleaned_data.get("status")
        delayed_date = cleaned_data.get("delayed_date")

        if status == 'Delayed' and not delayed_date:
            self.add_error('delayed_date', 'Delayed date is required when status is Delayed')
        return cleaned_data

class CashoutForm(forms.ModelForm):
    installment_details = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = Cashout
        fields = '__all__'
        
    def __init__(self, *args, **kwargs):
        super(CashoutForm, self).__init__(*args, **kwargs)
        self.fields['delayed_date'].widget.attrs['style'] = 'display:none;'
        if self.instance and self.instance.status == 'Delayed':
            self.fields['delayed_date'].widget.attrs['style'] = 'display:block;'
        if self.instance and self.instance.installment_details:
            self.fields['installment_details'].initial = json.dumps(self.instance.installment_details, indent=2)

    def clean(self):
        cleaned_data = super(CashoutForm, self).clean()
        status = cleaned_data.get("status")
        delayed_date = cleaned_data.get("delayed_date")
        installment_details = cleaned_data.get("installment_details")

        if status == 'Delayed' and not delayed_date:
            self.add_error('delayed_date', 'Delayed date is required when status is Delayed')
        
        if installment_details:
            try:
                installment_details_json = json.loads(installment_details)
                total_amount = Decimal(0)
                for installment in installment_details_json:
                    total_amount += Decimal(installment['amount'])
                cleaned_data['total_installment_amount'] = total_amount
                cleaned_data['balance_to_pay'] = cleaned_data.get('cash_out') - total_amount
                cleaned_data['installment_details'] = installment_details_json
            except json.JSONDecodeError:
                self.add_error('installment_details', 'Invalid JSON format')
        
        return cleaned_data
class CashInAdmin(admin.ModelAdmin):
    list_display = ['income_source', 'date', 'cash_in', 'status', 'delayed_date', 'project', 'cost_center', 'service_date']
    list_filter = ['status', 'cost_center', 'service_date']
    form = CashInForm

class CashoutAdmin(admin.ModelAdmin):
    list_display = ['expense_source', 'date', 'cash_out', 'status', 'delayed_date', 'remark', 'project', 'cost_center', 'service_date', 'total_installment_amount', 'balance_to_pay', 'installment_details']
    readonly_fields = ['total_installment_amount', 'balance_to_pay', 'installment_details']
    fields = ['expense_source', 'date', 'cash_out', 'status', 'delayed_date', 'remark', 'project', 'cost_center', 'service_date', 'total_installment_amount', 'balance_to_pay', 'installment_details']
    form = CashoutForm
class SummaryAdmin(admin.ModelAdmin):
    list_display = ('date', 'cash_in', 'cash_out', 'balance')
    search_fields = ['date']
    ordering = ['-date']

@receiver(post_save, sender=CashIn)
def update_project_summary_on_save_cash_in(sender, instance, created, **kwargs):
    if created:
        cash_flow = Decimal(instance.cash_in)
        ProjectSummary.objects.create(
            date=instance.date,
            project=instance.project,
            cash_in=cash_flow,
            cash_out=0,
            service_date=instance.service_date,
            balance=cash_flow
        )
    else:
        cash_in_transactions = CashIn.objects.filter(date=instance.date, project=instance.project)
        cash_in_total = cash_in_transactions.aggregate(total_cash_in=Sum('cash_in'))['total_cash_in'] or 0
        cash_out_total = Cashout.objects.filter(date=instance.date, project=instance.project).aggregate(total_cash_out=Sum('cash_out'))['total_cash_out'] or 0
        balance = cash_in_total - cash_out_total

        ProjectSummary.objects.filter(date=instance.date, project=instance.project).update(
            cash_in=cash_in_total,
            cash_out=cash_out_total,
            balance=balance,
            service_date=instance.service_date
        )

@receiver(post_save, sender=Cashout)
def update_project_summary_on_save_cash_out(sender, instance, created, **kwargs):
    if created and not instance.installment_details:
        cash_flow = Decimal(instance.cash_out)
        ProjectSummary.objects.create(
            date=instance.date,
            project=instance.project,
            cash_in=0,
            cash_out=cash_flow,
            service_date=instance.service_date,
            balance=-cash_flow
        )
    elif not instance.installment_details:
        cash_out_transactions = Cashout.objects.filter(date=instance.date, project=instance.project)
        cash_out_total = cash_out_transactions.aggregate(total_cash_out=Sum('cash_out'))['total_cash_out'] or 0
        cash_in_total = CashIn.objects.filter(date=instance.date, project=instance.project).aggregate(total_cash_in=Sum('cash_in'))['total_cash_in'] or 0
        balance = cash_in_total - cash_out_total

        ProjectSummary.objects.filter(date=instance.date, project=instance.project).update(
            cash_in=cash_in_total,
            cash_out=cash_out_total,
            balance=balance,
            service_date=instance.service_date
        )

@receiver(post_delete, sender=CashIn)
def update_project_summary_on_delete_cash_in(sender, instance, **kwargs):
    cash_in_transactions = CashIn.objects.filter(date=instance.date, project=instance.project)
    cash_in_total = cash_in_transactions.aggregate(total_cash_in=Sum('cash_in'))['total_cash_in'] or 0
    cash_out_total = Cashout.objects.filter(date=instance.date, project=instance.project).aggregate(total_cash_out=Sum('cash_out'))['total_cash_out'] or 0
    balance = cash_in_total - cash_out_total

    ProjectSummary.objects.filter(date=instance.date, project=instance.project).update(
        cash_in=cash_in_total,
        cash_out=cash_out_total,
        balance=balance
    )

@receiver(post_delete, sender=Cashout)
def update_project_summary_on_delete_cash_out(sender, instance, **kwargs):
    cash_in_total = CashIn.objects.filter(date=instance.date, project=instance.project).aggregate(total_cash_in=Sum('cash_in'))['total_cash_in'] or 0
    cash_out_transactions = Cashout.objects.filter(date=instance.date, project=instance.project)
    cash_out_total = cash_out_transactions.aggregate(total_cash_out=Sum('cash_out'))['total_cash_out'] or 0
    balance = cash_in_total - cash_out_total

    ProjectSummary.objects.filter(date=instance.date, project=instance.project).update(
        cash_in=cash_in_total,
        cash_out=cash_out_total,
        balance=balance
    )

class ProjectSummaryAdmin(admin.ModelAdmin):
    list_display = ('date', 'project', 'service_date', 'cash_in', 'cash_out', 'balance')
    list_filter = ('date', 'project', 'service_date')
    search_fields = ('project',)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    change_list_template = 'admin/cashflow/project_summary_change_list.html'

    def changelist_view(self, request, extra_context=None):
        cl = self.get_changelist_instance(request)
        queryset = cl.get_queryset(request)

        total_cash_in = Decimal(queryset.aggregate(total_cash_in=Sum('cash_in'))['total_cash_in'] or 0)
        total_cash_out = Decimal(queryset.aggregate(total_cash_out=Sum('cash_out'))['total_cash_out'] or 0)
        balance = total_cash_in - total_cash_out

        actual_balance = balance

        start_inventory = Decimal(0)
        end_inventory = Decimal(0)

        if request.method == 'POST':
            start_inventory_str = request.POST.get('start_inventory', '').strip()
            end_inventory_str = request.POST.get('end_inventory', '').strip()

            if not start_inventory_str:
                messages.error(request, "Please enter the start inventory amount.")
            elif not end_inventory_str:
                messages.error(request, "Please enter the end inventory amount.")
            else:
                try:
                    start_inventory = Decimal(start_inventory_str)
                    end_inventory = Decimal(end_inventory_str)
                except InvalidOperation:
                    messages.error(request, "Invalid inventory amount. Please enter a valid number.")

            actual_balance = balance - start_inventory + end_inventory

        extra_context = extra_context or {}
        extra_context['total_cash_in'] = total_cash_in
        extra_context['total_cash_out'] = total_cash_out
        extra_context['balance'] = balance
        extra_context['actual_balance'] = actual_balance
        extra_context['start_inventory'] = start_inventory
        extra_context['end_inventory'] = end_inventory

        return super().changelist_view(request, extra_context=extra_context)

admin.site.register(Cashout, CashoutAdmin)
admin.site.register(Summary, SummaryAdmin)
admin.site.register(ProjectSummary, ProjectSummaryAdmin)
admin.site.register(CustomUser)
admin.site.register(IncomeSource)
admin.site.register(ExpenseSource)
admin.site.register(Project)
admin.site.register(CashIn, CashInAdmin)
