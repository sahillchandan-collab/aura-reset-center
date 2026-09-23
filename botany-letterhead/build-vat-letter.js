// Builds the VAT Management Representation Letter on the Botany Properties letterhead, stamped.
// Usage: node build-vat-letter.js   (writes examples/Botany_Properties_VAT_Management_Representation_Letter.docx)
const fs = require('fs');
const path = require('path');
const { Document, Packer, Paragraph, TextRun, ImageRun, Header, Footer, AlignmentType, Table, TableRow, TableCell,
  WidthType, BorderStyle, ShadingType, LevelFormat, HorizontalPositionRelativeFrom, VerticalPositionRelativeFrom,
  TextWrappingType } = require('docx');

const A = (f) => path.join(__dirname, 'assets', f);
const GREEN = '283718';
const EMU = 914400;
const barH = (40 / 2550) * 8.5 * EMU;

const header = new Header({ children: [new Paragraph({ children: [new ImageRun({
  type: 'png', data: fs.readFileSync(A('letterhead-header-band.png')),
  transformation: { width: 816, height: Math.round(816 * 560 / 2550) },
  floating: {
    horizontalPosition: { relative: HorizontalPositionRelativeFrom.PAGE, offset: 0 },
    verticalPosition: { relative: VerticalPositionRelativeFrom.PAGE, offset: 0 },
    wrap: { type: TextWrappingType.TOP_AND_BOTTOM }, behindDocument: true, allowOverlap: true,
  },
})] })] });

const footer = new Footer({ children: [
  new Paragraph({ alignment: AlignmentType.CENTER,
    border: { top: { style: BorderStyle.SINGLE, size: 6, color: GREEN, space: 6 } }, spacing: { before: 0, after: 0 },
    children: [new TextRun({ text: 'BOTANY PROPERTIES L.L.C', bold: true, color: GREEN, size: 18, characterSpacing: 40 })] }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 40, after: 0 },
    children: [new TextRun({ text: 'Dubai, United Arab Emirates', color: '5A6B4A', size: 16 })] }),
  new Paragraph({ children: [new ImageRun({
    type: 'png', data: fs.readFileSync(A('letterhead-footer-bar.png')),
    transformation: { width: 816, height: 13 },
    floating: {
      horizontalPosition: { relative: HorizontalPositionRelativeFrom.PAGE, offset: 0 },
      verticalPosition: { relative: VerticalPositionRelativeFrom.PAGE, offset: Math.round(11 * EMU - barH) },
      wrap: { type: TextWrappingType.NONE }, behindDocument: true, allowOverlap: true,
    },
  })] }),
] });

const stamp = new ImageRun({
  type: 'png', data: fs.readFileSync(A('botany-stamp-for-documents.png')),
  transformation: { width: 150, height: 150, rotation: -8 },
  floating: {
    horizontalPosition: { relative: HorizontalPositionRelativeFrom.MARGIN, offset: Math.round(4.75 * EMU) },
    verticalPosition: { relative: VerticalPositionRelativeFrom.PARAGRAPH, offset: Math.round(0.1 * EMU) },
    wrap: { type: TextWrappingType.NONE }, allowOverlap: true, behindDocument: false,
  },
});

const P = (children, opts = {}) => new Paragraph({ spacing: { after: 120, line: 252 }, ...opts, children });
const T = (text, o = {}) => new TextRun({ text, ...o });
const bullet = (children) => P(children, { numbering: { reference: 'bullets', level: 0 }, spacing: { after: 60 } });
const numbered = (children, extra = {}) => P(children, { numbering: { reference: 'numbers', level: 0 }, alignment: AlignmentType.JUSTIFIED, spacing: { after: 120, line: 252 }, ...extra });
const keep = { keepNext: true, keepLines: true };

// Summary table (all amounts in AED)
const cols = [1560, 2000, 1400, 2000, 1400]; // sums to 8360 DXA
const cell = (text, { bold = false, right = false, head = false } = {}, i) => new TableCell({
  width: { size: cols[i], type: WidthType.DXA },
  shading: head ? { type: ShadingType.CLEAR, fill: 'E9EEE3', color: 'auto' } : undefined,
  margins: { top: 60, bottom: 60, left: 100, right: 100 },
  children: [new Paragraph({ alignment: right ? AlignmentType.RIGHT : AlignmentType.LEFT, spacing: { after: 0 }, keepNext: true, keepLines: true,
    children: [new TextRun({ text, bold: bold || head, size: 20, color: head ? GREEN : undefined })] })],
});
const row = (cells, o = {}) => new TableRow({ cantSplit: true, children: cells.map((t, i) => cell(t, { ...o, right: o.right ?? i > 0 }, i)) });
const table = new Table({
  width: { size: 8360, type: WidthType.DXA }, columnWidths: cols,
  rows: [
    row(['VAT Quarter', 'Amt excluding VAT', 'VAT', 'Amt including VAT', 'No. of Invoices'], { head: true }),
    row(['1st quarter', '86,100.00', '4,305.00', '90,405.00', '1']),
    row(['2nd quarter', '123,480.00', '6,174.00', '129,654.00', '2']),
    row(['3rd quarter', '81,972.00', '4,099.00', '86,071.00', '1']),
    row(['Total', '291,552.00', '14,578.00', '306,130.00', '4'], { bold: true }),
  ],
});

const body = [
  P([T('MANAGEMENT REPRESENTATION LETTER', { bold: true, size: 28, color: GREEN })], { spacing: { after: 40 }, ...keep }),
  P([T('VAT Return', { bold: true, size: 24, color: '5A6B4A' })], { spacing: { after: 240 } }),
  P([T('Date: 22/09/2026', { bold: true })]),
  P([T('To: Alif Accounting and Tax Consultants', { bold: true })]),
  P([T('Subject: Management Representation for UAE VAT Returns — 1st, 2nd and 3rd Tax Periods 2026', { bold: true, underline: {} })], { spacing: { before: 120, after: 200 } }),
  P([T('Dear Team,')]),
  P([T('In connection with the preparation and submission of the Value Added Tax (VAT) Returns of '), T('BOTANY PROPERTIES L.L.C', { bold: true }), T(' for the following tax periods:')], { alignment: AlignmentType.JUSTIFIED, ...keep }),
  bullet([T('1st Quarter: 01/12/2025 to 28/02/2026', { bold: true })]),
  bullet([T('2nd Quarter: 01/03/2026 to 31/05/2026', { bold: true })]),
  bullet([T('3rd Quarter: 01/06/2026 to 31/08/2026', { bold: true })]),
  P([T('we confirm and represent the following:')], { spacing: { before: 120, after: 140 } }),
  numbered([T('We confirm that, to the best of our knowledge, the accounting records, invoices, financial statements, documents and information provided for the preparation of the above VAT Returns are accurate, complete and reliable.')]),
  numbered([T('We confirm that all information and supporting documents reasonably required for the preparation of the VAT Returns, including sales invoices, purchase invoices and other relevant records, have been provided to Alif Accounting and Tax Consultants and, to the best of our knowledge, the information provided is true, complete and does not contain any material omission or misstatement.')]),
  numbered([T('We understand that the VAT Returns have been prepared based on the information, records and explanations made available to Alif Accounting and Tax Consultants. The preparation of the returns does not constitute an audit or independent verification of the underlying records or information.')]),
  numbered([T('We hereby confirm the following summary of taxable supplies and output VAT for the above tax periods, based on the information and supporting documents provided by us (all amounts in AED):')], keep),
  table,
  P([T('')], { spacing: { after: 60 } }),
  numbered([T('We confirm that there are no VAT related expenses to declare for the mentioned quarters; therefore, the VAT on sales represents the total payable amount.')]),
  numbered([T('We acknowledge that the VAT Returns for the 1st and 2nd tax periods above are being filed after their respective statutory due dates. We take full responsibility for this delay and accept that late filing penalties, fines and/or interest may be levied by the Federal Tax Authority (FTA) as a result. We confirm that Alif Accounting and Tax Consultants shall not be held liable for any penalties, fines or interest arising from the late filing of these returns, as the returns are being submitted strictly on the basis of instructions and information provided by us.', { bold: true })]),
  numbered([T('We hereby authorise Alif Accounting and Tax Consultants to prepare and submit the above VAT Returns on our behalf with the Federal Tax Authority (FTA), as applicable, based on the figures confirmed in this letter.')]),
  P([T('We confirm that the above representations are true and correct to the best of our knowledge and belief.')], { alignment: AlignmentType.JUSTIFIED, spacing: { before: 120, after: 240 } }),
  // Sign-off block, kept together on one page; the stamp floats in the clear space to its right.
  P([T('Yours faithfully,'), stamp], keep),
  P([T('For and on behalf of BOTANY PROPERTIES L.L.C', { bold: true })], { spacing: { before: 120, after: 200 }, ...keep }),
  P([T('Authorized Signatory: ', { bold: true }), T('_______________________')], keep),
  P([T('Designation: ', { bold: true }), T('_______________________________')], keep),
  P([T('Signature: ', { bold: true }), T('_________________________________')], keep),
  P([T('Date: ', { bold: true }), T('_____________________________________')]),
];

const doc = new Document({
  styles: { default: { document: { run: { font: 'Calibri', size: 22, color: '1A1A1A' } } } },
  numbering: { config: [
    { reference: 'bullets', levels: [{ level: 0, format: LevelFormat.BULLET, text: '•', alignment: AlignmentType.LEFT,
      style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] },
    { reference: 'numbers', levels: [{ level: 0, format: LevelFormat.DECIMAL, text: '%1.', alignment: AlignmentType.LEFT,
      style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] },
  ] },
  sections: [{
    properties: { page: { size: { width: 12240, height: 15840 },
      margin: { top: 3400, right: 1440, bottom: 1500, left: 1440, header: 0, footer: 500 } } },
    headers: { default: header }, footers: { default: footer },
    children: body,
  }],
});

const out = path.join(__dirname, 'examples', 'Botany_Properties_VAT_Management_Representation_Letter.docx');
Packer.toBuffer(doc).then(b => { fs.writeFileSync(out, b); console.log('written', out); });
