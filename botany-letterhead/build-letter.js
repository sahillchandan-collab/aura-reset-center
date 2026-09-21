const fs = require('fs');
const { Document, Packer, Paragraph, TextRun, ImageRun, Header, Footer, AlignmentType,
  HorizontalPositionRelativeFrom, VerticalPositionRelativeFrom, TextWrappingType, BorderStyle } = require('docx');

const GREEN = '283718';
const EMU = 914400;
const bandW = 8.5 * EMU, bandH = (560/2550) * 8.5 * EMU;   // full-bleed, keep aspect
const barH = (40/2550) * 8.5 * EMU;

const header = new Header({ children: [ new Paragraph({ children: [ new ImageRun({
  type: 'png', data: fs.readFileSync(__dirname+'/assets/letterhead-header-band.png'),
  transformation: { width: 816, height: Math.round(816*560/2550) },
  floating: {
    horizontalPosition: { relative: HorizontalPositionRelativeFrom.PAGE, offset: 0 },
    verticalPosition:   { relative: VerticalPositionRelativeFrom.PAGE,   offset: 0 },
    wrap: { type: TextWrappingType.TOP_AND_BOTTOM }, behindDocument: true, allowOverlap: true,
  },
})]})]});

const footer = new Footer({ children: [
  new Paragraph({ alignment: AlignmentType.CENTER,
    border: { top: { style: BorderStyle.SINGLE, size: 6, color: GREEN, space: 6 } },
    spacing: { before: 0, after: 0 },
    children: [ new TextRun({ text: 'BOTANY PROPERTIES L.L.C', bold: true, color: GREEN, size: 18, characterSpacing: 40 }) ] }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 40, after: 0 },
    children: [ new TextRun({ text: 'Dubai, United Arab Emirates', color: '5A6B4A', size: 16 }) ] }),
  new Paragraph({ children: [ new ImageRun({
    type: 'png', data: fs.readFileSync(__dirname+'/assets/letterhead-footer-bar.png'),
    transformation: { width: 816, height: 13 },
    floating: {
      horizontalPosition: { relative: HorizontalPositionRelativeFrom.PAGE, offset: 0 },
      verticalPosition:   { relative: VerticalPositionRelativeFrom.PAGE,   offset: Math.round(11*EMU - barH) },
      wrap: { type: TextWrappingType.NONE }, behindDocument: true, allowOverlap: true,
    },
  })]}),
]});

const P = (children, opts={}) => new Paragraph({ spacing: { after: 160, line: 276 }, ...opts, children });
const T = (text, o={}) => new TextRun({ text, ...o });
const blank = () => P([T('')]);

const body = [
  P([T('Date: ', {bold:true}), T('21/09/2026', {bold:true})]),
  P([T('To: ', {bold:true}), T('UAE Financial Intelligence Unit (FIU)', {bold:true})]),
  blank(),
  P([T('Subject: Authorization to Register in the goAML Reporting System', {bold:true, underline:{}})]),
  blank(),
  P([T('With reference to the subject matter above, we are writing to authorize the following individuals to register in the GoAML system on behalf of our company '), T('BOTANY PROPERTIES L.L.C', {bold:true}), T('.')], { alignment: AlignmentType.JUSTIFIED }),
  blank(),
  P([T('For the Admin Role: ', {bold:true}), T('SAHILL JARNAIL CHANDAN JARNAIL', {bold:true})]),
  P([T('For the User Role: ', {bold:true}), T('SAHILL JARNAIL CHANDAN JARNAIL', {bold:true})]),
  blank(),
  P([T('We appreciate your cooperation.')]),
  blank(),

  P([T('Yours sincerely,'), new ImageRun({
    type: 'png', data: fs.readFileSync(__dirname+'/assets/botany-stamp-for-documents.png'),
    transformation: { width: 150, height: 150, rotation: -8 },
    floating: {
      horizontalPosition: { relative: HorizontalPositionRelativeFrom.MARGIN, offset: Math.round(4.55*EMU) },
      verticalPosition:   { relative: VerticalPositionRelativeFrom.PARAGRAPH, offset: Math.round(0.05*EMU) },
      wrap: { type: TextWrappingType.NONE }, allowOverlap: true, behindDocument: false,
    },
  })]),
  blank(), blank(),
  P([T('Name: ', {bold:true}), T('SAHILL JARNAIL CHANDAN JARNAIL', {bold:true})]),
  P([T('Signature: ', {bold:true}), T('______________________________')]),
  P([T('Date: ', {bold:true}), T('21/09/2026', {bold:true})]),
];

const doc = new Document({
  styles: { default: { document: { run: { font: 'Calibri', size: 22, color: '1A1A1A' } } } },
  sections: [{
    properties: { page: {
      size: { width: 12240, height: 15840 },
      margin: { top: 3400, right: 1440, bottom: 1500, left: 1440, header: 0, footer: 500 },
    }},
    headers: { default: header }, footers: { default: footer },
    children: body,
  }],
});
Packer.toBuffer(doc).then(b => { fs.writeFileSync('Botany_Properties_GoAML_Authorisation_Letter_Stamped.docx', b); console.log('written'); });
