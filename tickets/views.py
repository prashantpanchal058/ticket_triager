from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Ticket
from .forms import TicketSubmitForm, TicketCorrectionForm

from ml.inference import predict


@login_required
def submit_ticket(request):
    if request.method == "POST":
        form = TicketSubmitForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.submitted_by = request.user

            result = predict(ticket.subject, ticket.body)
            ticket.category = result["category"]
            ticket.category_confidence = result["category_confidence"]
            ticket.urgency = result["urgency"]
            ticket.urgency_confidence = result["urgency_confidence"]

            ticket.save()
            messages.success(request, "Ticket submitted and triaged.")
            return redirect("ticket_list")
    else:
        form = TicketSubmitForm()
    return render(request, "tickets/ticket_form.html", {"form": form})


@login_required
def ticket_list(request):
    if request.user.is_staff:
        tickets = Ticket.objects.all()
    else:
        tickets = Ticket.objects.filter(submitted_by=request.user)

    status = request.GET.get("status")
    category = request.GET.get("category")
    if status:
        tickets = tickets.filter(status=status)
    if category:
        tickets = tickets.filter(category=category)

    return render(request, "tickets/ticket_list.html", {
        "tickets": tickets,
        "status_choices": Ticket.STATUS_CHOICES,
        "category_choices": Ticket.CATEGORY_CHOICES,
    })


@login_required
def ticket_detail(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)

    # Only staff or the ticket's own submitter can view it
    if not request.user.is_staff and ticket.submitted_by != request.user:
        messages.error(request, "You don't have permission to view that ticket.")
        return redirect("ticket_list")

    form = None
    if request.user.is_staff:
        if request.method == "POST":
            form = TicketCorrectionForm(request.POST, instance=ticket)
            if form.is_valid():
                form.save()
                messages.success(request, "Ticket updated.")
                return redirect("ticket_detail", pk=ticket.pk)
        else:
            form = TicketCorrectionForm(instance=ticket)

    return render(request, "tickets/ticket_detail.html", {
        "ticket": ticket,
        "form": form,
    })