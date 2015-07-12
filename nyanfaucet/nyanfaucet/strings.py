from django.utils.translation import ugettext as _

CONFIRMATION_MAIL_SUBJECT = _("Activate your NyanFaucet account")
CONFIRMATION_MAIL_BODY = _("""Greetings!

Please confirm your NyanFaucet registration by following this link: https://nyan.space${link}

If you did not register an account recently and did not expect this, please ignore this email.
You can reach the faucet operator here: faucet-admin@nyan.space""")

LOGIN_REQUIRED = _("Please sign in first.")
INVALID_ACTIVATION_LINK = _("You have followed an incorrect activation link, you have been logged out as a precaution.")
INVALID_SESSION = _("Your session is invalid, please sign in again.")
ACCOUNT_DISABLED = _("Your account has been disabled, please contact the faucet operator.")
ACCOUNT_NOT_FOUND = _("Could not find an account for this address, please double check the address or sign up for a new account.")
ACCOUNT_CONFIRMATION_SENT = _("We have sent you an email with a link, please follow it to confirm your registration.")
ACCOUNT_ACTIVATED = _("Your account is now fully enabled, have a lot of fun!")
ACCOUNT_ALREADY_ACTIVATED = _("Your account has already been activated.")
SAFE_ACCOUNT_NOT_YET_CONFIRMED = _('Your account has not been confirmed yet, please click the link that has been sent to your email address or <a data-no-instant href="%s" class="btn btn-warning">resend activation link</a>')

DICE_ALREADY_ROLLED = _("You already rolled the dice once this round!")

WITHDRAWAL_FAILED =_("Failed to issue transaction, please try again later. If the error persists, please send an email to the faucet operator! (see footer)")
