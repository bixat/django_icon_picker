class IconPicker {
  constructor(options) {
    this.searchInput = document.getElementById(options.searchInputId);
    this.selectedIcon = document.getElementById("selectedIcon");
    this.resultsDiv = document.getElementById("results");
    this.colorPicker = document.getElementById("color");
    this.savePath = options.savePath;
    this.selectedPrefix = "";
    this.form = document.getElementById(`${options.model}_form`);
    this.objectId = options.objectId;
    this.model = options.model;
    this.icon = "";
    this.usesCloudStorage = options.usesCloudStorage || false;
    this.storageType = options.storageType || 'FileSystemStorage';

    this.init();
  }

  init() {
    this.setupInitialIcon();
    this.setupEventListeners();
    this.showStorageInfo();
  }

  setupInitialIcon() {
    const currentValue = this.searchInput.value;

    if (!currentValue) {
      this.selectedIcon.src = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24'%3E%3Cpath fill='%23cccccc' d='M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z'/%3E%3C/svg%3E";
      return;
    }

    // Determine icon URL based on storage type and value format
    let iconUrl = this.getIconUrl(currentValue);
    this.selectedIcon.src = iconUrl;
  }

  getIconUrl(value) {
    if (!value) return "";

    // If it's already a full URL, use it
    if (value.startsWith('http://') || value.startsWith('https://')) {
      return value;
    }

    // If it's an Iconify icon format (contains colon)
    if (value.includes(':') && !value.endsWith('.svg')) {
      const color = this.colorPicker ? this.colorPicker.value.replace('#', '%23') : '';
      return `https://api.iconify.design/${value}.svg${color ? `?color=${color}` : ''}`;
    }

    // If it's a stored file path
    if (value.endsWith('.svg')) {
      // For cloud storage, we might need to fetch the URL
      if (this.usesCloudStorage) {
        this.fetchStoredIconUrl(value);
        // Return a placeholder while fetching
        return "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24'%3E%3Cpath fill='%23cccccc' d='M12 2v20l7-5V7l-7-5z'/%3E%3C/svg%3E";
      }

      // For local storage
      return value.startsWith('/') ? value : `/${value}`;
    }

    return value;
  }

  async fetchStoredIconUrl(filePath) {
    try {
      const response = await fetch(`/icon_picker/get-icon-url/?model=${this.model}&id=${this.objectId}`);
      const data = await response.json();

      if (data.url) {
        this.selectedIcon.src = data.url;
      }
    } catch (error) {
      console.warn('Failed to fetch stored icon URL:', error);
    }
  }

  showStorageInfo() {
    // Add visual indicator for storage type (optional)
    if (this.usesCloudStorage) {
      const storageIndicator = document.createElement('div');
      storageIndicator.className = 'storage-indicator';
      storageIndicator.textContent = `Using ${this.storageType}`;
      storageIndicator.style.cssText = `
        font-size: 11px;
        color: #666;
        margin-top: 2px;
        font-style: italic;
      `;

      const container = this.searchInput.parentNode;
      if (container && !container.querySelector('.storage-indicator')) {
        container.appendChild(storageIndicator);
      }
    }
  }

  setupEventListeners() {
    // Search input listener
    this.searchInput.addEventListener("input", () => {
      const query = this.searchInput.value;
      if (query.length > 2) {
        this.searchIcons(query);
      } else {
        this.resultsDiv.innerHTML = "";
      }
    });

    // Color picker listener
    if (this.colorPicker) {
      this.colorPicker.addEventListener("input", () => {
        this.updateSelectedIconColor();
      });
    }

    // Form submit listener
    if (this.form) {
      this.form.addEventListener("submit", (event) => {
        if (this.savePath && this.icon) {
          this.downloadAndSaveSvg();
        }
      });
    }
  }

  updateSelectedIconColor() {
    const currentValue = this.searchInput.value;
    if (currentValue && currentValue.includes(':') && !currentValue.endsWith('.svg')) {
      // Update Iconify icon with new color
      const color = this.colorPicker.value.replace('#', '%23');
      this.selectedIcon.src = `https://api.iconify.design/${currentValue}.svg?color=${color}`;
    }
  }

  async searchIcons(query) {
    try {
      const response = await fetch(
        `https://api.iconify.design/search?query=${encodeURIComponent(query)}&limit=10&start=0&prefix=${this.selectedPrefix}`
      );

      if (!response.ok) {
        throw new Error(`API request failed: ${response.status}`);
      }

      const data = await response.json();

      this.resultsDiv.innerHTML = "";

      if (data.icons && data.icons.length > 0) {
        const dropdownList = document.createElement("div");
        dropdownList.className = "icon-dropdown-list";

        data.icons.forEach((icon) => {
          const color = this.colorPicker ? this.colorPicker.value.replace("#", "%23") : '';
          const iconUrl = `https://api.iconify.design/${icon}.svg${color ? `?color=${color}` : ''}`;

          const dropdownItem = this.createDropdownItem(icon, iconUrl);
          dropdownList.appendChild(dropdownItem);
        });

        this.resultsDiv.appendChild(dropdownList);
      } else {
        this.showNoResults("No icons found for your search.");
      }
    } catch (error) {
      console.error("Search error:", error);
      this.showNoResults("Search failed. Please try again.");
    }
  }

  showNoResults(message) {
    this.resultsDiv.innerHTML = `<div style="padding: 10px; color: #666; text-align: center;">${message}</div>`;
  }

  createDropdownItem(icon, iconUrl) {
    const item = document.createElement("div");
    item.className = "icon-dropdown-item";

    const iconImg = document.createElement("img");
    iconImg.src = iconUrl;
    iconImg.className = "icon-preview";
    iconImg.alt = `Icon: ${icon}`;

    // Handle image load errors
    iconImg.addEventListener('error', () => {
      iconImg.src = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24'%3E%3Ctext x='12' y='12' text-anchor='middle' fill='%23999'%3E?%3C/text%3E%3C/svg%3E";
    });

    const iconText = document.createElement("span");
    iconText.textContent = icon;
    iconText.className = "icon-name";

    item.appendChild(iconImg);
    item.appendChild(iconText);

    item.addEventListener("click", () => {
      this.selectIcon(icon, iconUrl);
    });

    return item;
  }

  selectIcon(icon, iconUrl) {
    this.icon = icon;
    this.selectedIcon.src = iconUrl;
    this.resultsDiv.innerHTML = "";

    // Update the input value based on whether we're saving locally or not
    if (this.savePath) {
      // Will be updated after successful save
      this.searchInput.value = icon;
    } else {
      // Store the Iconify icon reference
      this.searchInput.value = icon;
    }
  }

  async downloadAndSaveSvg() {
    if (!this.icon) return;

    const color = this.colorPicker ? this.colorPicker.value : '';
    const params = new URLSearchParams({
      icon: this.icon,
      id: this.objectId,
      model: this.model
    });

    if (color) {
      params.append('color', color);
    }

    try {
      const response = await fetch(`/icon_picker/download-svg/?${params}`);

      if (response.ok) {
        const savedPath = await response.text();
        this.searchInput.value = savedPath;

        // Update the preview with the saved file
        if (this.usesCloudStorage) {
          this.fetchStoredIconUrl(savedPath);
        } else {
          this.selectedIcon.src = `/${savedPath}`;
        }

        this.showSuccess("Icon saved successfully!");
      } else {
        const errorData = await response.json().catch(() => ({ error: 'Save failed' }));
        this.showError(errorData.error || 'Failed to save icon');
      }
    } catch (error) {
      console.error("Save error:", error);
      this.showError("Network error while saving icon");
    }
  }

  showSuccess(message) {
    this.showMessage(message, 'success');
  }

  showError(message) {
    this.showMessage(message, 'error');
  }

  showMessage(message, type) {
    // Create or update message element
    let messageEl = document.getElementById('icon-picker-message');
    if (!messageEl) {
      messageEl = document.createElement('div');
      messageEl.id = 'icon-picker-message';
      messageEl.style.cssText = `
        padding: 8px 12px;
        margin: 5px 0;
        border-radius: 4px;
        font-size: 13px;
        position: relative;
      `;
      this.resultsDiv.parentNode.insertBefore(messageEl, this.resultsDiv);
    }

    messageEl.textContent = message;
    messageEl.className = `icon-picker-message ${type}`;

    // Style based on type
    if (type === 'success') {
      messageEl.style.cssText += 'background: #d4edda; color: #155724; border: 1px solid #c3e6cb;';
    } else {
      messageEl.style.cssText += 'background: #f8d7da; color: #721c24; border: 1px solid #f1aeb5;';
    }

    // Auto-hide after 3 seconds
    setTimeout(() => {
      if (messageEl && messageEl.parentNode) {
        messageEl.parentNode.removeChild(messageEl);
      }
    }, 3000);
  }
}