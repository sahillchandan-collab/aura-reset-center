/**
 * Yontro CRM: adds Google Sheets' calendar picker to every date column.
 * Run once: Extensions > Apps Script > paste this > Save > choose addDatePickers > Run.
 * Any column whose header contains 📅 gets the calendar, plus the Dashboard "Day to view" cell.
 */
function addDatePickers() {
  const ss = SpreadsheetApp.getActive();
  const rule = SpreadsheetApp.newDataValidation()
    .requireDate()
    .setAllowInvalid(false)
    .setHelpText('Double-click for a calendar')
    .build();
  let count = 0;
  ['Inbound', 'Outbound', 'Clients', 'Shoots'].forEach(function (name) {
    const sh = ss.getSheetByName(name);
    if (!sh) return;
    const headers = sh.getRange(1, 1, 1, sh.getLastColumn()).getValues()[0];
    headers.forEach(function (h, i) {
      if (String(h).indexOf('📅') !== -1) {
        sh.getRange(2, i + 1, sh.getMaxRows() - 1, 1).setDataValidation(rule);
        count++;
      }
    });
  });
  const db = ss.getSheetByName('Dashboard');
  if (db) {
    db.getRange('C3').setDataValidation(rule);
    count++;
  }
  SpreadsheetApp.getUi().alert('Calendar pickers added to ' + count + ' date fields.');
}
