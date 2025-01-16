class IconPicker {
  constructor(options) {
    this.searchInput = document.getElementById(options.searchInputId);
    this.selectedIcon = document.getElementById("selectedIcon");
    this.resultsDiv = document.getElementById("results");
    this.prefixDropdown = document.getElementById("prefixDropdown");
    this.colorPicker = document.getElementById("color");
    this.savePath = options.savePath;
    this.selectedPrefix = "";
    this.form = document.getElementById(`${options.model}_form`);
    this.objectId = options.objectId;
    this.model = options.model;
    this.icon = "";

    this.init();
  }

  init() {
    this.setupInitialIcon();
    this.setupEventListeners();
    this.fetchIconifyPrefixes();
  }

  setupInitialIcon() {
    this.selectedIcon.src = this.searchInput.value.endsWith(".svg")
      ? `/${this.searchInput.value}`
      : `https://api.iconify.design/${this.searchInput.value}.svg`;
  }

  setupEventListeners() {
    this.prefixDropdown.addEventListener("change", (event) => {
      this.selectedPrefix = event.target.value;
    });

    this.searchInput.addEventListener("input", () => {
      const query = this.searchInput.value;
      if (query.length > 2) {
        this.searchIcons(query);
      } else {
        this.resultsDiv.innerHTML = "";
      }
    });

    this.form.addEventListener("submit", (event) => {
      if (this.savePath) {
        this.downloadAndSaveSvg(
          `${this.icon}.svg&color=${this.colorPicker.value.replace("#", "%23")}`
        );
      }
      this.form.submit();
    });
  }

  async searchIcons(query) {
    const response = await fetch(
      `https://api.iconify.design/search?query=${encodeURIComponent(
        query
      )}&limit=10&start=0&prefix=${this.selectedPrefix}`
    );
    const data = await response.json();

    this.resultsDiv.innerHTML = "";
    if (data.icons.length > 0) {
      const dropdownList = document.createElement("div");
      dropdownList.className = "icon-dropdown-list";

      data.icons.forEach((icon) => {
        const iconName = icon.replace(":", "-");
        const color = this.colorPicker.value.replace("#", "%23");
        const iconBaseUrl = `https://api.iconify.design/${icon}.svg`;
        const iconUrl = `${iconBaseUrl}?color=${color}`;

        const dropdownItem = this.createDropdownItem(icon, iconUrl);
        dropdownList.appendChild(dropdownItem);
      });

      this.resultsDiv.appendChild(dropdownList);
    } else {
      this.resultsDiv.textContent = "No icons found.";
    }
  }

  createDropdownItem(icon, iconUrl) {
    const item = document.createElement("div");
    item.className = "icon-dropdown-item";

    const iconImg = document.createElement("img");
    iconImg.src = iconUrl;
    iconImg.className = "icon-preview";

    const iconText = document.createElement("span");
    iconText.textContent = icon;
    iconText.className = "icon-name";

    item.appendChild(iconImg);
    item.appendChild(iconText);

    item.addEventListener("click", () => {
      this.searchInput.value = icon;
      this.selectedIcon.src = iconUrl;
      this.resultsDiv.innerHTML = "";
      this.icon = this.searchInput.value;
      if (this.savePath) {
        this.searchInput.value =
          this.savePath + `/${this.model}/icon-${this.objectId}.svg`;
      } else {
        this.searchInput.value = icon;
      }
    });

    return item;
  }

  fetchIconifyPrefixes() {
    fetch("https://api.iconify.design/collections?pretty=1")
      .then((response) => response.json())
      .then((data) => {
        const prefixes = Object.keys(data);
        this.populatePrefixDropdown(prefixes);
      })
      .catch((error) => console.error("Error fetching icon sets:", error));
  }

  populatePrefixDropdown(prefixes) {
    const selectElement = document.createElement("select");
    selectElement.id = "prefixDropdown";
    selectElement.className = "form-select block";

    prefixes.forEach((prefix) => {
      const option = document.createElement("option");
      option.value = prefix;
      option.textContent = prefix;
      selectElement.appendChild(option);
    });

    this.prefixDropdown.appendChild(selectElement);
  }

  downloadAndSaveSvg(svgIcon) {
    const downloadUrl = `/icon_picker/download-svg/?icon=${svgIcon}&id=${this.objectId}&model=${this.model}`;
    fetch(downloadUrl)
      .then((response) => response.text())
      .then((data) => {
        this.searchInput.value = data;
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  }
}
