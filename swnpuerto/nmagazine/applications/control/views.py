from django.shortcuts import render
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import HttpResponseRedirect

from django.views.generic import (
    ListView,
)

from applications.control.models import DetailVoucher


class VoucherGuideListView(ListView):
    context_object_name = 'vouchers'
    template_name = 'admin/control/voucher_guides.html'

    def get_queryset(self):
        guide = self.kwargs['guide']
        print '==========='
        print guide
        return DetailVoucher.objects.filter(
            anulate=False,
            guide__pk=guide,
        )
