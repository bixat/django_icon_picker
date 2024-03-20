 document.addEventListener("DOMContentLoaded", function () {
        const selectedIcon = document.getElementById("selectedIcon");
      const searchInput = document.getElementById("{{ widget_id }}");
      selectedIcon.src = `https://api.iconify.design/${searchInput.value}.svg?color=grey`;
      const resultsDiv = document.getElementById("results");
      let selectedPrefix = "";
      
      document
        .getElementById("prefixDropdown")
        .addEventListener("change", function (event) {
          selectedPrefix = event.target.value;
        });
      searchInput.addEventListener("input", function () {
        const query = searchInput.value;
        if (query.length > 2) {
          searchIcons(query, resultsDiv, selectedPrefix);
        } else {
          resultsDiv.innerHTML = "";
        }
      });
    });

    async function searchIcons(query, resultsDiv, selectedPrefix) {
      const response = await fetch(
        `https://api.iconify.design/search?query=${encodeURIComponent(
          query
        )}&limit=10&start=0&prefix=${selectedPrefix}`
      );
      const data = await response.json();

      resultsDiv.innerHTML = "";
      const searchInput = document.getElementById("{{ widget_id }}");
      if (data.icons.length > 0) {
        data.icons.forEach((icon) => {
          const iconName = icon.replace(":", "-");
          const iconUrl = `https://api.iconify.design/${icon}.svg?color=grey`
          const iconImg = document.createElement("img");
          iconImg.src = iconUrl;
          iconImg.className = "{{ widget.attrs.icons_class }}";
          iconImg.addEventListener("click", function () {
            searchInput.value = iconName;
            resultsDiv.innerHTML = "";
            selectedIcon.src = iconUrl;
          });
          
          resultsDiv.appendChild(iconImg);
        });
      } else {
        resultsDiv.textContent = "No icons found.";
      }
    }
    function fetchIconifyPrefixes() {
      fetch("https://api.iconify.design/collections?pretty=1")
        .then((response) => response.json())
        .then((data) => {
          const prefixes = Object.keys(data);
          populatePrefixDropdown(prefixes);
        })
        .catch((error) => console.error("Error fetching icon sets:", error));
    }

    function populatePrefixDropdown(prefixes) {
      const dropdownContainer = document.getElementById(
        "prefixDropdown"
      );
      const selectElement = document.createElement("select");
      selectElement.id = "prefixDropdown";
      selectElement.className = "form-select block {{ widget.attrs.class }}";

      prefixes.forEach((prefix) => {
        const option = document.createElement("option");
        option.value = prefix;
        option.textContent = prefix;
        selectElement.appendChild(option);
      });

      dropdownContainer.appendChild(selectElement);
    }
    fetchIconifyPrefixes();