import random
import pandas as pd

random.seed(42)

ticket_templates = {
    "billing": [
        ("Payment failed", "My payment was declined while trying to complete my order."),
        ("Card was charged twice", "I was charged twice for the same purchase. Please check and refund the duplicate charge."),
        ("Unexpected charge", "I noticed a charge on my card that I do not recognize."),
        ("Invoice is incorrect", "The amount shown on my invoice does not match what I expected to pay."),
        ("Payment pending", "My payment has been pending for a long time. Can you check its status?"),
        ("Wrong amount charged", "The amount charged to my card is different from the amount shown at checkout."),
        ("Card payment not reflected", "My card was charged but the order still shows as unpaid."),
        ("Need billing receipt", "Could you please send me the receipt for my recent purchase?"),
        ("Promo discount missing", "The promotional discount was not applied to my order."),
        ("Tax amount is wrong", "The tax amount on my invoice appears to be incorrect."),
    ],

    "account": [
        ("Can't login", "I am unable to log into my account even though I am entering the correct password."),
        ("Password reset link not working", "The password reset link I received does not work."),
        ("Forgot password", "I forgot my password and need help resetting it."),
        ("Account locked", "My account has been locked and I cannot access it."),
        ("Change email address", "I want to update the email address associated with my account."),
        ("Change phone number", "I need to change the phone number on my account."),
        ("Unable to verify account", "The account verification process keeps failing."),
        ("Account information incorrect", "Some of my account information is incorrect and I need to update it."),
        ("Two-factor authentication issue", "I am not receiving the verification code for two-factor authentication."),
        ("Deactivate account", "I would like to deactivate my account."),
    ],

    "orders": [
        ("Order not showing", "I placed an order but it is not appearing in my order history."),
        ("Cancel my order", "I want to cancel my order before it is shipped."),
        ("Wrong item ordered", "I accidentally ordered the wrong item and would like to change it."),
        ("Order confirmation missing", "I placed an order but never received an order confirmation."),
        ("Order status unclear", "The status of my order has not changed and I am not sure what is happening."),
        ("Order quantity incorrect", "The order shows a different quantity than what I selected."),
        ("Need to modify order", "I need to change some details on my recent order."),
        ("Order was cancelled", "My order was cancelled unexpectedly. Please explain why."),
        ("Duplicate order", "It looks like my order was submitted twice."),
        ("Order history missing", "Some of my previous orders are missing from my account."),
    ],

    "shipping": [
        ("Package is late", "My package was supposed to arrive earlier but it has not arrived yet."),
        ("Tracking not updating", "The tracking information has not been updated for several days."),
        ("Package delivered but missing", "The tracking says delivered but I have not received the package."),
        ("Wrong delivery address", "My package is being sent to the wrong address."),
        ("Shipping delay", "There is a delay with my shipment and I need an update."),
        ("Package damaged", "My package arrived damaged. What should I do?"),
        ("Missing package", "My shipment appears to be missing and I cannot locate it."),
        ("Delivery date changed", "The estimated delivery date keeps changing."),
        ("Courier issue", "The courier was unable to deliver my package."),
        ("Tracking number invalid", "The tracking number provided does not show any information."),
    ],

    "refund": [
        ("Refund not received", "My refund was approved but I have not received the money yet."),
        ("Request a refund", "I would like to request a refund for my recent purchase."),
        ("Refund amount incorrect", "The refund I received is less than the amount I originally paid."),
        ("Refund pending", "My refund has been pending for several days."),
        ("Refund for cancelled order", "My order was cancelled but I have not received my refund."),
        ("Duplicate payment refund", "I was charged twice and need a refund for the duplicate payment."),
        ("Return refund missing", "I returned the item but have not received my refund."),
        ("Refund to wrong card", "The refund does not appear to have been sent to my original payment method."),
        ("Partial refund", "I only received part of the refund I was expecting."),
        ("Refund status", "Can you tell me the current status of my refund?"),
    ],

    "technical": [
        ("Website not loading", "The website is not loading for me and keeps showing an error."),
        ("App keeps crashing", "The mobile app crashes every time I try to open it."),
        ("Page not responding", "The page becomes unresponsive when I try to complete my purchase."),
        ("Error message", "I keep receiving an error message while using the service."),
        ("Feature not working", "One of the features is not working as expected."),
        ("Upload failed", "I am unable to upload my file and the upload keeps failing."),
        ("Search not working", "The search function is not returning any results."),
        ("Slow website", "The website is extremely slow today."),
        ("App login issue", "I cannot log into the mobile app even though the website works."),
        ("Checkout error", "I get an error whenever I try to proceed to checkout."),
    ],

    "product": [
        ("Product unavailable", "The product I want is currently unavailable. Do you know when it will be back?"),
        ("Wrong product received", "I received a different product from the one I ordered."),
        ("Product damaged", "The product arrived damaged and I would like a replacement."),
        ("Product missing parts", "The product I received is missing some parts."),
        ("Product quality issue", "The quality of the product is not what I expected."),
        ("Product description incorrect", "The product does not match the description shown on the website."),
        ("Need product information", "I need more information about the product before purchasing."),
        ("Product compatibility", "Can you confirm whether this product is compatible with my device?"),
        ("Size is incorrect", "The size I received is different from the size I ordered."),
        ("Product stopped working", "The product stopped working shortly after I received it."),
    ],

    "subscription": [
        ("Cancel subscription", "I want to cancel my current subscription."),
        ("Subscription renewed unexpectedly", "My subscription renewed even though I did not intend to renew it."),
        ("Subscription payment failed", "My subscription payment failed and I need help resolving it."),
        ("Upgrade subscription", "I would like to upgrade my current subscription plan."),
        ("Downgrade subscription", "I want to downgrade my subscription to a cheaper plan."),
        ("Subscription not activated", "I paid for a subscription but it has not been activated."),
        ("Subscription charged twice", "I was charged twice for my subscription this month."),
        ("Free trial ended", "I was charged after my free trial ended and I was not expecting it."),
        ("Subscription benefits missing", "Some benefits included in my subscription are not available."),
        ("Subscription renewal date", "Can you tell me when my subscription will renew?"),
    ],
}

urgency_map = {
    "billing": ["medium", "high", "high", "medium", "low"],
    "account": ["medium", "high", "medium", "high", "low"],
    "orders": ["medium", "high", "medium", "low", "high"],
    "shipping": ["medium", "high", "medium", "low", "high"],
    "refund": ["medium", "high", "medium", "high", "low"],
    "technical": ["medium", "high", "medium", "low", "high"],
    "product": ["low", "medium", "medium", "high", "low"],
    "subscription": ["medium", "high", "medium", "low", "high"],
}

# Extra phrases to make tickets more varied
openings = [
    "Hi,",
    "Hello support,",
    "Hi team,",
    "Hello,",
    "Dear support team,"
]

closings = [
    "Please help me with this.",
    "Could you please look into this?",
    "I would appreciate your help.",
    "Please let me know what I should do.",
    "Can you check this for me?"
]

tickets = []

for i in range(400):
    category = random.choice(list(ticket_templates.keys()))
    subject, body = random.choice(ticket_templates[category])
    urgency = random.choice(urgency_map[category])

    # Add natural variation
    body = (
        f"{random.choice(openings)} "
        f"{body} "
        f"{random.choice(closings)}"
    )

    tickets.append({
        "subject": subject,
        "body": body,
        "category": category,
        "urgency": urgency
    })

df = pd.DataFrame(tickets)

# Shuffle the dataset
df = df.sample(frac=1, random_state=42).reset_index(drop=True)

# Save CSV
df.to_csv("support_tickets_400.csv", index=False)

print(df.head(10))
print("\nDataset shape:", df.shape)
print("\nCategory distribution:")
print(df["category"].value_counts())

print("\nUrgency distribution:")
print(df["urgency"].value_counts())

print("\nSaved as: support_tickets_400.csv")