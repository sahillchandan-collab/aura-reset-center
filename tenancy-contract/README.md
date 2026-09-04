# Tenancy contract – additional conditions (addendum)

`build_addendum.py` regenerates the Botany "additional conditions" pages of the
long-term tenancy contract and splices them into an issued Ejari contract PDF.

```
pip install pymupdf reportlab
python3 build_addendum.py <original_contract.pdf> <output_contract.pdf>
```

Pages 1–3 (Ejari unified contract) and the final Botany cover page are copied
from the original unchanged; the addendum pages in between are rebuilt from the
clauses in the script as a blank template: deposit, rent, broker and renewal
fees, cheque dates and amounts, permitted occupants and the daily late-payment
charge are fill-in lines. The number of occupant / payment lines and the fixed
figures (AED 1,000 minor-maintenance cap, AED 1,000 bounced-cheque penalty)
are in the `OPTIONS` dict at the top of the script.

`additional_conditions.pdf` is the current addendum output on its own.
Montserrat fonts are bundled under `fonts/` (SIL Open Font License).
