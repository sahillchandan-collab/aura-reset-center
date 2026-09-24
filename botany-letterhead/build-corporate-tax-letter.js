// Builds the Corporate Tax Management Representation Letter on the Botany Properties letterhead, stamped.
// Usage: node build-corporate-tax-letter.js
//   (writes examples/Botany_Properties_Corporate_Tax_Management_Representation_Letter.docx)
const fs = require('fs');
const path = require('path');
const { Document, Packer, Paragraph, TextRun, ImageRun, Header, Footer, AlignmentType, BorderStyle, LevelFormat,
  HorizontalPositionRelativeFrom, VerticalPositionRelativeFrom, TextWrappingType } = require('docx');

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
const numbered = (children, extra = {}) => P(children, { numbering: { reference: 'numbers', level: 0 }, alignment: AlignmentType.JUSTIFIED, spacing: { after: 120, line: 252 }, keepLines: true, ...extra });
const keep = { keepNext: true, keepLines: true };

const body = [
  P([T('MANAGEMENT REPRESENTATION LETTER', { bold: true, size: 28, color: GREEN })], { spacing: { after: 40 }, ...keep }),
  P([T('Corporate Tax Return', { bold: true, size: 24, color: '5A6B4A' })], { spacing: { after: 240 } }),
  P([T('Date: 22/09/2026', { bold: true })]),
  P([T('To: Alif Accounting and Tax Consultants', { bold: true })]),
  P([T('Subject: Management Representation for UAE Corporate Tax Return', { bold: true, underline: {} })], { spacing: { before: 120, after: 200 } }),
  P([T('Dear Team,')]),
  P([T('In connection with the preparation and submission of the Corporate Tax Return '), T('BOTANY PROPERTIES L.L.C', { bold: true }), T(' for the tax period ended 31/12/2025, we confirm and represent the following:')], { alignment: AlignmentType.JUSTIFIED, spacing: { after: 160 }, ...keep }),
  numbered([T('We confirm that, to the best of our knowledge, the accounting records, financial statements, documents and information provided for the preparation of the Corporate Tax Return are accurate, complete and reliable.')]),
  numbered([T('We confirm that all information and supporting documents reasonably required for the preparation of the Corporate Tax Return have been provided to Alif Accounting and Tax Consultants and, to the best of our knowledge, the information provided is true, complete and does not contain any material omission or misstatement.')]),
  numbered([T('We understand that the Corporate Tax Return has been prepared based on the information, records and explanations made available to Alif Accounting and Tax Consultants. The preparation of the return does not constitute an audit or independent verification of the underlying records or information.')]),
  numbered([T('Based on the information currently available to us, there is no known intention or decision to liquidate the Company, cease its operations or significantly curtail its activities, except where such matters have been separately communicated or disclosed.')]),
  numbered([T('We acknowledge that the Corporate Tax Return is prepared in accordance with the applicable UAE Corporate Tax Law and based on the information and explanations provided. We understand that any tax treatment adopted may be affected by the completeness and accuracy of the information and supporting documents made available for the preparation of the return.')]),
  numbered([T('We hereby confirm that the total revenue of the company for the relevant tax period amounted to AED 263,490 based on the information and supporting documents provided by us.', { bold: true })]),
  numbered([T('We hereby authorise Alif Accounting and Tax Consultants to assist with the preparation and submission of the Corporate Tax Return on our behalf. We further request Alif Accounting and Tax Consultants to file the Corporate Tax Return under the UAE Small Business Relief regime, subject to the applicable eligibility conditions and requirements.')]),
  numbered([T('We understand that the accuracy and completeness of the information and supporting documents provided are important for the correct preparation of the Corporate Tax Return. Where any additional tax, penalties, interest or other consequences arise as a result of information that was inaccurate, incomplete, subsequently changed, or not made available to Alif Accounting and Tax Consultants, such matters may fall outside the scope of the services provided by Alif Accounting and Tax Consultants.')]),
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

const out = path.join(__dirname, 'examples', 'Botany_Properties_Corporate_Tax_Management_Representation_Letter.docx');
Packer.toBuffer(doc).then(b => { fs.writeFileSync(out, b); console.log('written', out); });
