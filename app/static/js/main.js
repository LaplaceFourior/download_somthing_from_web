const form = document.querySelector('form');
const urlInput = document.querySelector('#url');
const submitButton = document.querySelector('#submit');
const list = document.createElement('ul');
const resultDiv = document.createElement('div');

const createLoadingScreen = () => {
  const loadingScreen = document.createElement('div');
  loadingScreen.style = `
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
  `;
  loadingScreen.innerHTML = 'Scanning, please wait...';
  document.body.appendChild(loadingScreen);
  urlInput.disabled = true;
  submitButton.disabled = true;
  return loadingScreen;
};

const handleCheckboxChange = (event) => {
  const valueList = event.target.parentNode.querySelector('ul');
  if (valueList) {
    const valueCheckboxes = valueList.querySelectorAll('input[type="checkbox"]');
    valueCheckboxes.forEach(valueCheckbox => {
      valueCheckbox.checked = event.target.checked;
    });
  }
};

const handleDownloadButtonClick = (event) => {
  const button = event.target;
  const keyName = button.parentNode.getAttribute('id');
  const valueCheckboxes = button.parentNode.querySelectorAll('input[type="checkbox"]');
  const selectedValues = { [keyName]: [] };
  valueCheckboxes.forEach((valueCheckbox, index) => {
    if (valueCheckbox.checked) {
      selectedValues[keyName].push(index);
    }
  });

  const data = { selectedValues };

  button.disabled = true; // disable the button before making the fetch request
  button.innerHTML = 'Downloading...'; // set the button text to "Downloading..."

  const cancelButton = document.createElement('button'); // create a new button element for canceling the download
  cancelButton.innerHTML = 'Cancel Download'; // set the button text to "Cancel Download"
  cancelButton.style = 'margin-left: 10px;'; // set the button style
  cancelButton.addEventListener('click', () => {
    controller.abort(); // abort the fetch request
    button.disabled = false; // enable the download button again
    button.innerHTML = 'Download'; // set the button text back to "Download"
    cancelButton.parentNode.removeChild(cancelButton); // remove the cancel button
  });
  button.parentNode.appendChild(cancelButton); // append the cancel button to the button's parent node

  const statusSpan = document.createElement('span'); // create a new span element for the status
  statusSpan.style = 'margin-left: 10px; color: blue;'; // set the style of the status span
  statusSpan.innerHTML = 'Downloading'; // set the initial text of the status span
  button.parentNode.appendChild(statusSpan); // append the status span to the button's parent node

  const controller = new AbortController(); // create a new AbortController for the fetch request
  const signal = controller.signal; // get the signal from the AbortController

  const download = () => {
    fetch('/download', {
      method: 'POST',
      body: JSON.stringify(data),
      headers: {
        'Content-Type': 'application/json',
        'User-Agent': navigator.userAgent
      },
      signal // pass the signal to the fetch request
    })
      .then(response => {
        button.innerHTML = 'Download'; // set the button text back to "Download"
        statusSpan.innerHTML = 'Downloaded Successfully'; // set the status span text to "Downloaded Successfully"
        statusSpan.style.color = 'green'; // set the color of the status span to green
        cancelButton.parentNode.removeChild(cancelButton); // remove the cancel button
        return response.json();
      })
      .catch(error => {
        button.innerHTML = 'Download'; // set the button text back to "Download"
        statusSpan.innerHTML = 'Download Failed'; // set the status span text to "Download Failed"
        statusSpan.style.color = 'red'; // set the color of the status span to red
        console.error(error);
        // setTimeout(download, 1000); // try again after 1 second
      })
      .finally(() => {
        button.disabled = false; // enable the button again
      });
  };

  download();
};

const handleFormSubmit = (event) => {
  event.preventDefault();
  const url = urlInput.value;
  const loadingScreen = createLoadingScreen();

  fetch('/submit-url', {
    method: 'POST',
    body: JSON.stringify({ url }),
    headers: {
      'Content-Type': 'application/json'
    }
  })
    .then(response => response.json())
    .then(({ links }) => {
      document.body.removeChild(loadingScreen);
      urlInput.disabled = false;
      submitButton.disabled = false;

      resultDiv.innerHTML = 'Scanning Result';
      resultDiv.style = `
        width: 100%;
        padding: 10px;
        border: 1px solid #ccc;
        border-radius: 5px;
        box-sizing: border-box;
        margin-bottom: 20px;
      `;
      form.parentNode.insertBefore(resultDiv, form.nextSibling);
      resultDiv.appendChild(list);

      for (const [keyName, valueList] of Object.entries(links)) {
        const keyItem = document.createElement('li');
        const keyDiv = document.createElement('div');
        keyDiv.innerHTML = keyName;
        keyDiv.setAttribute('id', keyName);
        keyDiv.setAttribute('type', 'filename');
        keyItem.appendChild(keyDiv);

        const keyCheckbox = document.createElement('input');
        keyCheckbox.type = 'checkbox';
        keyCheckbox.addEventListener('change', handleCheckboxChange);
        keyDiv.appendChild(keyCheckbox);

        const keyDownloadButton = document.createElement('button');
        keyDownloadButton.innerHTML = 'Download';
        keyDownloadButton.style = 'margin-left: 10px;';
        keyDownloadButton.type = 'Download';
        keyDownloadButton.addEventListener('click', handleDownloadButtonClick);
        keyDiv.appendChild(keyDownloadButton);

        const valueUl = document.createElement('ul');
        for (const value of valueList) {
          const valueItem = document.createElement('li');
          const valueCheckbox = document.createElement('input');
          valueCheckbox.type = 'checkbox';
          const valueName = value.substring(value.lastIndexOf('/') + 1);
          const valueSpan = document.createElement('span');
          valueSpan.innerHTML = valueName;
          valueItem.appendChild(valueCheckbox);
          valueItem.appendChild(valueSpan);
          valueUl.appendChild(valueItem);
        }
        keyDiv.appendChild(valueUl);
        list.appendChild(keyItem);
      }
    })
    .catch(error => {
      if (document.body.contains(loadingScreen)) {
        document.body.removeChild(loadingScreen);
      }
      urlInput.disabled = false;
      submitButton.disabled = false;
      console.error(error);
    })
    .finally(() => {
      form.reset(); // reset the form
      location.reload(); // reload the page
    });
};

submitButton.addEventListener('click', handleFormSubmit);