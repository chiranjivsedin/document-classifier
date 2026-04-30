export const classifyDocument = async (file) => {
  if (!file) throw new Error("No file provided");

  const formData = new FormData();
  formData.append('file', file);

  const response = await fetch('/classify', {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    let errMsg = `Server returned ${response.status}: ${response.statusText}`;
    try {
      const errBody = await response.json();
      if (errBody.detail) errMsg = errBody.detail;
    } catch (e) {
      // JSON parse error, ignore and use default message
    }
    throw new Error(errMsg);
  }

  return response.json();
};
