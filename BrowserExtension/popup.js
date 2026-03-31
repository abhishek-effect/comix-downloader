document.addEventListener('DOMContentLoaded', async () => {
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  const themeToggle = document.getElementById('theme-toggle');
  const imgCountSpan = document.getElementById('img-count');
  const tabTitleDiv = document.getElementById('tab-title');

  // 1. Set Title
  tabTitleDiv.innerText = tab.title;

  // 2. Load/Save Theme
  chrome.storage.local.get('theme', (data) => {
    if (data.theme === 'dark') {
      document.body.setAttribute('data-theme', 'dark');
      themeToggle.checked = true;
    }
  });

  themeToggle.addEventListener('change', () => {
    const mode = themeToggle.checked ? 'dark' : 'light';
    document.body.setAttribute('data-theme', mode);
    chrome.storage.local.set({ theme: mode });
  });

  // 3. Get Image Count from Content Script
  chrome.tabs.sendMessage(tab.id, { action: "analyze" }, (response) => {
    if (response && response.count) {
      imgCountSpan.innerText = response.count;
    }
  });

  // 4. Download Logic
  document.getElementById('startBtn').addEventListener('click', () => {
    chrome.tabs.sendMessage(tab.id, { action: "get_urls" }, (response) => {
      if (response && response.urls) {
        response.urls.forEach((url, index) => {
          chrome.downloads.download({
            url: url,
            filename: `MangaDownloads/${tab.title.replace(/[^a-z0-9]/gi, '_')}/${index + 1}.webp`
          });
        });
      }
    });
  });
});
