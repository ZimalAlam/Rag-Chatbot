import PdfUploader from "../components/PdfUploader";

export default function Home() {
  return (
    <div style={{ padding: "20px" }}>
      <h2>Document Upload</h2>
      <PdfUploader />
    </div>
  );
}
