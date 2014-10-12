var page = require('webpage').create(), system = require('system');

if (system.args.length <3) {
  console.log('Usage: html2pdf.js <pdf_url> <pdf_root> <project_id>');
  phantom.exit();
}

var pdf_url = system.args[1]
var pdf_root = system.args[2]
var project_id = system.args[3]
console.log("pdf_url:"+pdf_url);
console.log("project_id:"+project_id);
//page.viewportSize = { width: 1024, height : 3000 };
page.paperSize = {
    format: 'A4',
    orientation: 'portrait',
    margin: '0.8cm' ,
/* default header/footer for pages that don't have custom overwrites (see below) */
        header: {
            height: "1cm",
            contents: phantom.callback(function(pageNum, numPages) {
                if (pageNum == 1) {
                    return "";
                }
                return "<h1>Header <span style='float:right'>" + pageNum + " / " + numPages + "</span></h1>";
            })
        },
        footer: {
            height: "1cm",
            contents: phantom.callback(function(pageNum, numPages) {
                if (pageNum == numPages) {
                    return "";
                }
                return "<h1>Footer <span style='float:right'>" + pageNum + " / " + numPages + "</span></h1>";
            })
        }};
//page.content = '<html><body><p id="surface">hello world王小儿！</p></body></html>';
t = Date.now();
page.open(pdf_url, function() {
  //page.render('github.png');
//  page.render('../../media/submission.pdf');
//    'E:/workspace/smartwifi/media/submission'
  page.render(pdf_root+project_id+'.pdf');
  t = Date.now() - t;
  console.log('Loading time ' + t + ' msec');
  phantom.exit();
});
