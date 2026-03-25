import html2canvas from 'html2canvas';
import { jsPDF } from 'jspdf';
import logoUrl from '../assets/logo.png';

export async function exportToPdf(element, pageName) {
  if (!element) return;

  // Make sure full content is visible by forcing components to resize to content
  const detailBody = element.querySelector('.detail-body');
  const origBodyCssText = detailBody ? detailBody.style.cssText : '';
  const origElCssText = element.style.cssText;

  if (detailBody) {
    detailBody.style.overflowY = 'visible';
    detailBody.style.height = 'auto';
    detailBody.style.flex = 'none';
  }
  element.style.height = 'auto';
  element.style.minHeight = 'auto';

  try {
    const canvas = await html2canvas(element, {
      scale: 2, // High resolution
      useCORS: true,
      logging: false,
      backgroundColor: '#ffffff' // Ensure background is white
    });

    const imgData = canvas.toDataURL('image/png');

    const pdf = new jsPDF({
      orientation: 'portrait',
      unit: 'mm',
      format: 'a4'
    });

    const pageWidth = pdf.internal.pageSize.getWidth();
    const pageHeight = pdf.internal.pageSize.getHeight();

    const imgProps = pdf.getImageProperties(imgData);
    const imgHeight = (imgProps.height * pageWidth) / imgProps.width;

    let heightLeft = imgHeight;
    let position = 0;

    // Watermark Logo dimensions and position
    const logoW = 80;
    const logoH = 80;
    const logoX = (pageWidth - logoW) / 2;
    const logoY = (pageHeight - logoH) / 2;

    // Timestamp
    const now = new Date();
    const dd = String(now.getDate()).padStart(2, '0');
    const mm = String(now.getMonth() + 1).padStart(2, '0');
    const yyyy = now.getFullYear();
    const hh = String(now.getHours()).padStart(2, '0');
    const min = String(now.getMinutes()).padStart(2, '0');
    const ss = String(now.getSeconds()).padStart(2, '0');
    const timestampStr = `Downloaded: ${dd}-${mm}-${yyyy} ${hh}:${min}:${ss}`;

    const addWatermarkAndHeaderFooter = () => {
      pdf.setGState(new pdf.GState({ opacity: 0.15 }));
      pdf.addImage(logoUrl, 'PNG', logoX, logoY, logoW, logoH);
      pdf.setGState(new pdf.GState({ opacity: 1.0 }));

      pdf.setFontSize(8);
      pdf.setTextColor(100);
      pdf.text(timestampStr, pageWidth - 10, pageHeight - 8, { align: 'right' });
    };

    // Render First page
    pdf.addImage(imgData, 'PNG', 0, position, pageWidth, imgHeight);
    addWatermarkAndHeaderFooter();
    heightLeft -= pageHeight;

    // Render Subsequent pages if remaining content exceeds current page
    while (heightLeft > 0) {
      position -= pageHeight;
      pdf.addPage();
      pdf.addImage(imgData, 'PNG', 0, position, pageWidth, imgHeight);
      addWatermarkAndHeaderFooter();
      heightLeft -= pageHeight;
    }

    const fileName = `dparis_${pageName}_${dd}${mm}${yyyy}.pdf`;
    pdf.save(fileName);
  } catch (err) {
    console.error("PDF Export Error:", err);
    alert("Gagal mengunduh PDF. Silakan coba lagi.");
  } finally {
    // Restore styles back to original
    if (detailBody) {
      detailBody.style.cssText = origBodyCssText;
    }
    element.style.cssText = origElCssText;
  }
}
