chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  const progressDiv = document.querySelector('div[class*="progress-line"]');
  const firstImg = document.querySelector('img.fit-w');
  const spanCount = progressDiv ? progressDiv.querySelectorAll('span').length : 0;

  if (request.action === "analyze") {
    sendResponse({ count: spanCount });
  }

  if (request.action === "get_urls") {
    if (!firstImg || spanCount === 0) {
      sendResponse({ urls: null });
      return;
    }

    const baseSrc = firstImg.src;
    const lastSlashIndex = baseSrc.lastIndexOf('/');
    const basePath = baseSrc.substring(0, lastSlashIndex);
    
    const imageUrls = [];
    for (let i = 1; i <= spanCount; i++) {
      const pageNum = i.toString().padStart(2, '0');
      imageUrls.push(`${basePath}/${pageNum}.webp`);
    }
    sendResponse({ urls: imageUrls });
  }
});
