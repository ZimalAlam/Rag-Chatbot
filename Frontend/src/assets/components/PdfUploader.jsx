import { useState } from "react";
import { uploadPDFs } from "../api/apiClient";

export default function PdfUploader() {
  const [files, setFiles] = useState([]);

  const handleUpload = async () => {
    if (!files.length) return alert("Select PDFs first");
    await uploadPDFs(files);
    alert("PDFs processed!");
  };

  return (
    <div style={styles.box}>
      <h3>Upload PDFs</h3>
      <input
        type="file"
        multiple
        accept=".pdf"
        onChange={(e) => setFiles([...e.target.files])}
      />
      <button onClick={handleUpload}>Upload</button>
    </div>
  );
}

const styles = {
  box: {
    marginBottom: "20px",
  },
};
