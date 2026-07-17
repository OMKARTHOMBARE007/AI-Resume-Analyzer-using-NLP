import { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { FiUploadCloud, FiFile, FiX, FiCheck } from 'react-icons/fi';
import './FileUpload.css';

export default function FileUpload({ onFileSelect, accept = '.pdf,.docx', maxSize = 10 }) {
  const [selectedFile, setSelectedFile] = useState(null);
  const [error, setError] = useState('');

  const onDrop = useCallback((acceptedFiles, rejectedFiles) => {
    setError('');

    if (rejectedFiles.length > 0) {
      const rejection = rejectedFiles[0];
      if (rejection.errors[0]?.code === 'file-too-large') {
        setError(`File too large. Max size: ${maxSize}MB`);
      } else if (rejection.errors[0]?.code === 'file-invalid-type') {
        setError('Invalid file type. Please upload PDF or DOCX files.');
      } else {
        setError('Invalid file. Please try again.');
      }
      return;
    }

    if (acceptedFiles.length > 0) {
      const file = acceptedFiles[0];
      setSelectedFile(file);
      onFileSelect(file);
    }
  }, [onFileSelect, maxSize]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
    },
    maxSize: maxSize * 1024 * 1024,
    multiple: false,
  });

  const removeFile = (e) => {
    e.stopPropagation();
    setSelectedFile(null);
    onFileSelect(null);
  };

  const formatSize = (bytes) => {
    if (bytes < 1024) return `${bytes} B`;
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
    return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
  };

  return (
    <div className="file-upload-wrapper">
      <div
        {...getRootProps()}
        className={`dropzone ${isDragActive ? 'dropzone-active' : ''} ${selectedFile ? 'dropzone-has-file' : ''}`}
      >
        <input {...getInputProps()} />

        {selectedFile ? (
          <div className="selected-file">
            <div className="file-icon">
              <FiFile size={28} />
            </div>
            <div className="file-details">
              <span className="file-name">{selectedFile.name}</span>
              <span className="file-size">{formatSize(selectedFile.size)}</span>
            </div>
            <div className="file-status">
              <FiCheck size={18} className="check-icon" />
            </div>
            <button className="remove-file" onClick={removeFile}>
              <FiX size={16} />
            </button>
          </div>
        ) : (
          <div className="dropzone-content">
            <div className="upload-icon-wrapper">
              <FiUploadCloud size={40} />
            </div>
            <h3>{isDragActive ? 'Drop your file here' : 'Drag & drop your resume'}</h3>
            <p>or <span className="browse-text">browse files</span></p>
            <div className="file-hints">
              <span className="badge badge-blue">PDF</span>
              <span className="badge badge-purple">DOCX</span>
              <span className="hint-text">Max {maxSize}MB</span>
            </div>
          </div>
        )}
      </div>

      {error && (
        <div className="alert alert-error" style={{ marginTop: '12px' }}>
          {error}
        </div>
      )}
    </div>
  );
}
