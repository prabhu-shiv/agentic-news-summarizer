// build_report.js
// Called by reporter.py via subprocess
// Usage: node build_report.js <articles_json_path> <output_docx_path> <report_config_path>

const {
  Document, Packer, Paragraph, TextRun,
  AlignmentType
} = require("docx");
const fs = require("fs");

// --- Load inputs ---
const articlesPath = process.argv[2];
const outputPath   = process.argv[3];
const configPath   = process.argv[4];

const articles = JSON.parse(fs.readFileSync(articlesPath, "utf8"));
const cfg      = JSON.parse(fs.readFileSync(configPath,   "utf8"));

// --- pt to half-points (docx-js uses half-points for font size) ---
const pt = (n) => n * 2;

// --- Helper: one paragraph with a bold label + normal value on same line ---
function labeledParagraph(label, value) {
  return new Paragraph({
    spacing: { after: cfg.spacing.after_section_dxa },
    children: [
      new TextRun({
        text: label,
        bold: true,
        size: pt(cfg.section_label.size_pt),
        font: cfg.font,
        color: cfg.color
      }),
      new TextRun({
        text: value || "N/A",
        bold: false,
        size: pt(cfg.section_body.size_pt),
        font: cfg.font,
        color: cfg.color
      })
    ]
  });
}

// --- Build document children ---
const children = [];

// ── Report header ──
children.push(
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { after: 200 },
    children: [
      new TextRun({
        text: cfg.report_header.text,
        bold: cfg.report_header.bold,
        size: pt(cfg.report_header.size_pt),
        font: cfg.font,
        color: cfg.color
      })
    ]
  })
);

// ── Date line ──
const today = new Date().toLocaleDateString("en-US", {
  year: "numeric", month: "long", day: "numeric"
});
children.push(
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { after: 200 },
    children: [
      new TextRun({
        text: `Generated: ${today}`,
        bold: false,
        size: pt(11),
        font: cfg.font,
        color: cfg.color
      })
    ]
  })
);

// ── Article count line ──
children.push(
  new Paragraph({
    spacing: { after: 400 },
    children: [
      new TextRun({
        text: `${articles.length} article(s) passed the relevance threshold (${cfg.relevance_threshold || 7}/10).`,
        bold: false,
        italics: true,
        size: pt(11),
        font: cfg.font,
        color: cfg.color
      })
    ]
  })
);

// ── Articles ──
articles.forEach((article, index) => {

  // Title — 13pt Bold
  children.push(
    new Paragraph({
      spacing: { after: cfg.spacing.after_title_dxa },
      children: [
        new TextRun({
          text: `${index + 1}. ${article.title}`,
          bold: cfg.title.bold,
          size: pt(cfg.title.size_pt),
          font: cfg.font,
          color: cfg.color
        })
      ]
    })
  );

  // Source
  children.push(labeledParagraph("Source: ", article.source));

  // Relevance Score
  children.push(labeledParagraph("Relevance Score: ", `${article.relevance_score} / 10`));

  // What happened
  children.push(labeledParagraph("What happened: ", article.summary));

  // Why it matters to Intel
  children.push(labeledParagraph("Why it matters to Intel: ", article.why_it_matters));

  // Link
  children.push(labeledParagraph("Link: ", article.link));

  // Blank spacer between articles
  children.push(
    new Paragraph({
      spacing: { after: cfg.spacing.after_article_dxa },
      children: [
        new TextRun({ text: "" })
      ]
    })
  );
});

// ── Assemble document ──
const doc = new Document({
  sections: [{
    properties: {
      page: {
        size: {
          width:  cfg.page.width_dxa,
          height: cfg.page.height_dxa
        },
        margin: {
          top:    cfg.page.margin_dxa,
          bottom: cfg.page.margin_dxa,
          left:   cfg.page.margin_dxa,
          right:  cfg.page.margin_dxa
        }
      }
    },
    children
  }]
});

Packer.toBuffer(doc)
  .then((buffer) => {
    fs.writeFileSync(outputPath, buffer);
    console.log(`[Reporter] Report saved to: ${outputPath}`);
  })
  .catch((err) => {
    console.error("[Reporter] ERROR building document:", err);
    process.exit(1);
  });