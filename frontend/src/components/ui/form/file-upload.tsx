interface FileUploadProps {
  label?: string;
  onFileSelect: (file: File) => void;
  accept?: string;
}

export function FileUpload({ label, onFileSelect, accept }: FileUploadProps) {
  const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      onFileSelect(file);
    }
  };

  return (
    <div className="mb-4">
      {label && (
        <label className="block text-sm font-medium mb-1">{label}</label>
      )}
      <input
        type="file"
        onChange={handleChange}
        accept={accept}
        className="w-full"
      />
    </div>
  );
} 