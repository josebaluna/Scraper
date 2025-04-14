const puppeteer = require('puppeteer');

async function scrapeAllPages() {
  const browser = await puppeteer.launch({ headless: true });
  const page = await browser.newPage();
  let auctions = [];

  try {
    const baseUrl = 'https://subastas.boe.es/subastas_ava.php?accion=Mas&id_busqueda=_ODdKcDhuSjJ2UGhTZ2pJd3RpdUlYYjlXZy9KeGxNTHpoVE9PWjEzdWw4OE5jaG9QanZIZnFScUJYRzFhc0g3bXZXTmFDSktxbUFwc2M1RGwwVytpaDBacVY1K0YwempyWXRpTkJnSUdoMENzOGR3Z1VoNG1GbjhLNmFieEhwNEFIRHlUeFZFWjN3N1d2VUJ2WktnM3kxN09iSDhhTzVnaWJhZmJhTTNMNldpcnZ0UWtzSko5M0JxV0NBb1h5L0JqOUtveHdmTnNQZ3V6c043SE9hbmtKUXNRYXU3VUVhYWNaQVBYMTJJWm1hRHNZcXQrUmFGVVJjTjIyZFE5ZmxOdg,,';
    const resultsPerPage = 500;
    const maxPages = 3; // Número máximo de páginas a procesar

    for (let i = 0; i < maxPages; i++) {
      const offset = i * resultsPerPage;
      const url = `${baseUrl}-${offset}-${resultsPerPage}`;

      console.log(`Scraping URL: ${url}`);
      await page.goto(url, { waitUntil: 'domcontentloaded' });

      // Esperar un tiempo adicional para asegurar que la página se cargue completamente
      await new Promise(resolve => setTimeout(resolve, 1500)); // 1,5 segundos

      // Esperar a que se carguen los resultados
      try {
        await page.waitForSelector('li.resultado-busqueda');
        console.log(`Resultados cargados para la página ${i + 1}.`);

        // Capturar los datos de las subastas en la página actual
        const auctionsOnPage = await page.evaluate(() => {
          const auctionsList = [];
          document.querySelectorAll('li.resultado-busqueda').forEach(auction => {
            let title = auction.querySelector('h3') ? auction.querySelector('h3').innerText.trim().replace(/^SUBASTA\s*/, '') : 'N/A';
            let court = auction.querySelector('h4') ? auction.querySelector('h4').innerText.trim() : 'N/A';
            let caseNumber = 'N/A';
            let status = 'N/A';
            let description = 'N/A';

            let paragraphs = auction.querySelectorAll('p');
            Array.from(paragraphs).forEach(p => {
              if (p.innerText.includes('Expediente')) {
                caseNumber = p.innerText.trim().replace('Expediente: ', '');
              } else if (p.innerText.includes('Estado')) {
                status = p.innerText.trim().replace('Estado: ', '');
              } else {
                description = p.innerText.trim();
              }
            });

            let detailLink = auction.querySelector('a.resultado-busqueda-link-defecto') ? auction.querySelector('a.resultado-busqueda-link-defecto').getAttribute('href') : '';
            let detailUrl = detailLink ? new URL(detailLink, 'https://subastas.boe.es/').href.replace(/&idBus=.*/, '') : 'N/A';

            auctionsList.push({
              title,
              court,
              caseNumber,
              status,
              description,
              detailUrl
            });
          });
          return auctionsList;
        });

        // Agregar las subastas de la página actual a la lista principal
        auctions = auctions.concat(auctionsOnPage);
        console.log(`Página ${i + 1} procesada. Subastas encontradas: ${auctionsOnPage.length}`);
      } catch (error) {
        console.error(`Error al extraer datos en la página ${i + 1}:`, error);
      }
    }

    return auctions;
  } catch (error) {
    console.error("Error en el scraping con Puppeteer:", error);
    return [];
  } finally {
    await browser.close();
  }
}

scrapeAllPages().then(auctions => {
  if (auctions.length > 0) {
    const fs = require('fs');
    fs.writeFileSync('all_auctions.json', JSON.stringify(auctions, null, 2));
    console.log("Datos de todas las subastas guardados en 'all_auctions.json'.");
  } else {
    console.log("No se encontraron subastas para guardar.");
  }
}).catch(error => {
  console.error("Error en el script de scraping:", error);
});
