// Builds the FTA penalty reconsideration and waiver request on the Botany Properties letterhead, stamped.
// Usage: node build-fta-waiver-letter.js
//   (writes examples/Botany_Properties_FTA_Penalty_Waiver_Request.docx)
const fs = require('fs');
const path = require('path');
const { Document, Packer, Paragraph, TextRun, ImageRun, Header, Footer, AlignmentType, BorderStyle, Table, TableRow,
  TableCell, WidthType, ShadingType, VerticalAlign, HorizontalPositionRelativeFrom, VerticalPositionRelativeFrom,
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
    horizontalPosition: { relative: HorizontalPositionRelativeFrom.MARGIN, offset: Math.round(4.85 * EMU) },
    verticalPosition: { relative: VerticalPositionRelativeFrom.PARAGRAPH, offset: Math.round(-0.55 * EMU) },
    wrap: { type: TextWrappingType.NONE }, allowOverlap: true, behindDocument: false,
  },
});

const P = (children, opts = {}) => new Paragraph({ spacing: { after: 110, line: 252 }, ...opts, children });
const T = (text, o = {}) => new TextRun({ text, ...o });
const keep = { keepNext: true, keepLines: true };

// Penalty table
const cols = [1500, 3500, 2160, 1200]; // sums to 8360 DXA (full text width)
const cell = (text, i, { head = false } = {}) => new TableCell({
  width: { size: cols[i], type: WidthType.DXA },
  verticalAlign: VerticalAlign.CENTER,
  shading: head ? { type: ShadingType.CLEAR, fill: 'E9EEE3', color: 'auto' } : undefined,
  margins: { top: 70, bottom: 70, left: 100, right: 100 },
  children: [new Paragraph({ alignment: i === 3 ? AlignmentType.RIGHT : (i === 1 ? AlignmentType.LEFT : AlignmentType.CENTER),
    spacing: { after: 0 }, keepNext: true, keepLines: true,
    children: [new TextRun({ text, bold: head, size: 19, color: head ? GREEN : undefined })] })],
});
const row = (cells, o) => new TableRow({ cantSplit: true, tableHeader: !!(o && o.head), children: cells.map((t, i) => cell(t, i, o)) });
const latePay = 'Failure of the Taxable Person to settle the Payable Tax within the timeframe specified in the Tax Law';
const lateFile = 'Failure of the Registrant to submit the Tax Return within the timeframe specified in the Tax Law.';
const table = new Table({
  width: { size: 8360, type: WidthType.DXA }, columnWidths: cols,
  rows: [
    row(['Transaction Number', 'Liability Type', 'Period Description', 'Debit (AED)'], { head: true }),
    row(['230011708752', latePay, 'Stagger 2 Period 1 - Mar 2026 to May 2026', '216.09']),
    row(['230011674806', latePay, 'Stagger 2 Period 4 - Dec 2025 to Feb 2026', '301.38']),
    row(['36700173705', lateFile, 'Stagger 2 Period 1 - Mar 2026 to May 2026', '2,000.00']),
    row(['33800339460', lateFile, 'Stagger 2 Period 4 - Dec 2025 to Feb 2026', '1,000.00']),
  ],
});

const body = [
  P([T('Date: ', { bold: true }), T('24/09/2026')]),
  P([T('To: The Federal Tax Authority, United Arab Emirates', { bold: true })]),
  P([T('Subject: Request for Reconsideration and Waiver of Penalty for Late VAT Filing and Payment', { bold: true, underline: {} })], { spacing: { before: 80, after: 180 } }),
  P([T('Dear Sir/Madam,')]),
  P([T('We respectfully submit this request for reconsideration of the penalty imposed on '), T('BOTANY PROPERTIES L.L.C', { bold: true }), T(' due to Late VAT Filing and Payment for the following:')], { alignment: AlignmentType.JUSTIFIED }),
  P([T('Taxable Person Name: ', { bold: true }), T('BOTANY PROPERTIES L.L.C')], { spacing: { after: 40 }, ...keep }),
  P([T('TRN: ', { bold: true }), T('104507623700003')], { spacing: { after: 160 }, ...keep }),
  table,
  P([T('')], { spacing: { after: 60 } }),
  P([T('The delay in filing and payment of the VAT return was unintentional. At the time, we were not fully aware of the applicable filing and payment requirements and the relevant deadline. Once we became aware of the requirement, we took the necessary steps to complete the VAT filing and payment. We assure you that the required compliance procedures are now in place to ensure that future VAT returns and payments are completed within the prescribed deadlines. In light of the above, we kindly request the Federal Tax Authority to reconsider the matter and waive the penalty imposed.')], { alignment: AlignmentType.JUSTIFIED }),
  P([T('We sincerely appreciate your understanding and favourable consideration.')], { spacing: { after: 220 } }),
  // Sign-off; the stamp floats in the clear space to its right.
  P([T('Yours faithfully,'), stamp], keep),
  P([T('BOTANY PROPERTIES L.L.C', { bold: true })]),
];

const doc = new Document({
  styles: { default: { document: { run: { font: 'Calibri', size: 22, color: '1A1A1A' } } } },
  sections: [{
    properties: { page: { size: { width: 12240, height: 15840 },
      margin: { top: 3400, right: 1440, bottom: 1500, left: 1440, header: 0, footer: 500 } } },
    headers: { default: header }, footers: { default: footer },
    children: body,
  }],
});

const out = path.join(__dirname, 'examples', 'Botany_Properties_FTA_Penalty_Waiver_Request.docx');
Packer.toBuffer(doc).then(b => { fs.writeFileSync(out, b); console.log('written', out); });
