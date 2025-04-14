const fs = require('fs');
const puppeteer = require('puppeteer');

const TIMEOUT = 6000; // Tiempo de espera de 6 segundos
const RETRY_LIMIT = 3; // Número de intentos antes de abandonar

async function scrapeDetails(url) {
    const browser = await puppeteer.launch({ headless: true });
    const page = await browser.newPage();

    // Deshabilitar la carga de imágenes y otros recursos no esenciales
    await page.setRequestInterception(true);
    page.on('request', (request) => {
        if (['image', 'stylesheet', 'font', 'media'].includes(request.resourceType())) {
            request.abort();
        } else {
            request.continue();
        }
    });

    // Opcional: Deshabilitar JavaScript para acelerar la carga
    await page.setJavaScriptEnabled(false);

    const auctionDetails = { url };

    try {
        // Iterar a través de las pestañas
        for (let tab = 1; tab <= 4; tab++) {
            await page.goto(`${url}&ver=${tab}`, { waitUntil: 'load', timeout: TIMEOUT });
            const details = await page.evaluate(() => {
                const result = {};
                const rows = Array.from(document.querySelectorAll('table tbody tr'));
                rows.forEach(row => {
                    const key = row.querySelector('th')?.innerText.trim();
                    const value = row.querySelector('td')?.innerText.trim();
                    if (key && value) {
                        result[key] = value;
                    }
                });
                return result;
            });

            // Guardar los detalles generales de la subasta
            if (tab !== 3) {
                Object.assign(auctionDetails, details);
            }

            // Si estamos en la pestaña de "Lotes" (ver=3)
            if (tab === 3) {
                // Extraer todos los enlaces de las sub-pestañas de lotes
                const lotUrls = await page.evaluate(() => {
                    const lotLinks = Array.from(document.querySelectorAll('#tabsver ul.navlistver li a'));
                    return lotLinks.length > 0 ? lotLinks.map(link => link.href) : null;
                });

                if (lotUrls) {
                    // Iterar sobre cada sub-pestaña de lote y extraer detalles
                    for (let lotUrl of lotUrls) {
                        const lotId = new URL(lotUrl).searchParams.get('idLote');
                        await page.goto(lotUrl, { waitUntil: 'load', timeout: TIMEOUT });
                        const lotDetails = await page.evaluate(() => {
                            const result = {};
                            const rows = Array.from(document.querySelectorAll('table tbody tr'));
                            rows.forEach(row => {
                                const key = row.querySelector('th')?.innerText.trim();
                                const value = row.querySelector('td')?.innerText.trim();
                                if (key && value) {
                                    result[key] = value;
                                }
                            });
                            return result;
                        });

                        auctionDetails[`Lote_${lotId}`] = lotDetails;
                    }
                } else {
                    // Si no hay sub-pestañas, extraer detalles de la única pestaña de lote disponible
                    const lotId = 1;  // Asignamos 1 como identificador del lote único
                    const lotDetails = await page.evaluate(() => {
                        const result = {};
                        const rows = Array.from(document.querySelectorAll('table tbody tr'));
                        rows.forEach(row => {
                            const key = row.querySelector('th')?.innerText.trim();
                            const value = row.querySelector('td')?.innerText.trim();
                            if (key && value) {
                                result[key] = value;
                            }
                        });
                        return result;
                    });

                    auctionDetails[`Lote_${lotId}`] = lotDetails;
                }
            }
        }

        return auctionDetails;
    } catch (error) {
        console.error(`Error en la URL ${url}: ${error}`);
        return null;
    } finally {
        await browser.close();
    }
}

async function saveDetails(details) {
    const filePath = 'all_details.json';
    let allDetails = [];

    if (fs.existsSync(filePath)) {
        const fileContent = fs.readFileSync(filePath, 'utf-8');
        allDetails = JSON.parse(fileContent);
    }

    allDetails.push(details);
    fs.writeFileSync(filePath, JSON.stringify(allDetails, null, 2));
    console.log(`Datos guardados para la URL ${details.url}`);
}

async function processUrlsSequentially(urls) {
    for (let url of urls) {
        const result = await retryScrapeDetails(url, RETRY_LIMIT);
        if (result !== null) {
            await saveDetails(result);
        }
    }
}

async function retryScrapeDetails(url, retries) {
    for (let attempt = 1; attempt <= retries; attempt++) {
        const result = await scrapeDetails(url);
        if (result !== null) {
            return result;
        }
        console.log(`Reintentando (${attempt}/${retries}) para la URL ${url}`);
    }
    console.error(`Falló la URL ${url} después de ${retries} intentos`);
    return null;
}

// Leer las URLs desde el archivo urls.txt generado por el script Python
const urls = fs.readFileSync('urls.txt', 'utf-8').split('\n').filter(url => url.trim() !== '');

processUrlsSequentially(urls);
