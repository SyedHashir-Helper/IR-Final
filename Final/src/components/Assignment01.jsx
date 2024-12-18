import React, { useState } from 'react';
import { useForm, Controller } from 'react-hook-form';
import axios from 'axios';
import { 
  FileAddOutlined, 
  LoadingOutlined, 
  CheckCircleOutlined,
  FileTextOutlined
} from '@ant-design/icons';
import { Select } from 'antd'; // Make sure to install antd
import "../styles/Assignment01.css"

const FileUploadForm = () => {
  const [files, setFiles] = useState([]);
  const [loading, setLoading] = useState(false);
  const [documentsProcessed, setDocumentsProcessed] = useState(false);
  const [submitSuccess, setSubmitSuccess] = useState(false);
  const [responseFiles, setResponseFiles] = useState([]);

  const { 
    register, 
    handleSubmit, 
    formState: { errors }, 
    control,
    setValue 
  } = useForm({
    defaultValues: {
      searchType: 'boolean' // Default to content search
    }
  });

  const handleFileChange = async (e) => {
    const uploadedFiles = Array.from(e.target.files)
      .filter(file => file.name.endsWith('.txt'));

    const filesWithContent = uploadedFiles.map(file => {
      const reader = new FileReader();
      return new Promise((resolve) => {
        reader.onload = (event) => {
          resolve({
            filename: file.name,
            content: event.target.result
          });
        };
        reader.readAsText(file);
      });
    });

    try {
      const processedFiles = await Promise.all(filesWithContent);
      setFiles(processedFiles);

      // First API call to process documents
      setLoading(true);
      const payload = { files: processedFiles };
      
      const response = await axios.post('http://localhost:5000/api/documents/upload', payload);

      console.log('Documents Processed:', response.data);
      setDocumentsProcessed(true);
      setLoading(false);
    } catch (error) {
      console.error('Document processing error:', error);
      setLoading(false);
      alert('Error processing documents. Please try again.');
    }
  };

  const onSubmit = async (data) => {
    if (!documentsProcessed) {
      alert('Please wait for documents to be processed first.');
      return;
    }

    setLoading(true);
    setResponseFiles([]);
    
    try {
      const payload = {
        query: data.query,
        searchType: data.searchType // Add search type to payload
      };

      const response = await axios.post(`http://localhost:5000/api/search/${data.searchType}`, payload);

      console.log('Query Response:', response.data);
      
      // Expecting response in the format: [{ title: "", content: "" }]
      setResponseFiles(response.data || []);
      setLoading(false);
      setSubmitSuccess(true);
      
      // Reset form after 3 seconds
      setTimeout(() => {
        setSubmitSuccess(false);
      }, 3000);

    } catch (error) {
      setLoading(false);
      console.error('Query submission error:', error);
      alert('Error processing your query. Please try again.');
    }
  };

  const downloadFile = (file) => {
    const blob = new Blob([file.content], { type: 'text/plain' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = file.title || 'downloaded-file.txt';
    a.click();
    window.URL.revokeObjectURL(url);
  };

  return (
    <div className="form-container">
      <form onSubmit={handleSubmit(onSubmit)}>
        {/* File Upload */}
        <div className="form-group">
          <label>Upload TXT Files</label>
          <div className="file-upload-wrapper">
            <label className="file-upload-label">
              <FileAddOutlined className="upload-icon" />
              <p>Select multiple .txt files</p>
              <input 
                type="file" 
                multiple 
                accept=".txt"
                className="file-input"
                onChange={handleFileChange}
              />
            </label>
          </div>
        </div>

        {/* Uploaded Files List */}
        {files.length > 0 && (
          <div className="uploaded-files">
            <h4>Uploaded Files:</h4>
            <ul>
              {files.map((file, index) => (
                <li key={index}>{file.filename}</li>
              ))}
            </ul>
          </div>
        )}

        {/* Search Type Selection */}
        <div className="form-group">
          <label>Search Type</label>
          <Controller
            name="searchType"
            control={control}
            render={({ field }) => (
              <Select
                {...field}
                style={{ width: '100%' }}
                disabled={!documentsProcessed}
              >
                <Select.Option value="boolean" disabled>Boolean</Select.Option>
                {/* <Select.Option value="title">Title</Select.Option> */}
              </Select>
            )}
          />
        </div>

        {/* Query Input */}
        <div className="form-group">
          <label>Query</label>
          <input 
            type="text"
            placeholder="Enter your query"
            {...register('query', { 
              required: 'Query is required',
              minLength: {
                value: 3,
                message: 'Query must be at least 3 characters'
              }
            })}
            className="query-input"
            disabled={!documentsProcessed}
          />
          {errors.query && (
            <p className="error-message">
              {errors.query.message}
            </p>
          )}
        </div>

        {/* Submit Button */}
        <button 
          type="submit" 
          disabled={loading || !documentsProcessed}
          className={`submit-button ${loading ? 'loading' : ''}`}
        >
          {loading ? (
            <span>
              <LoadingOutlined /> Processing...
            </span>
          ) : (
            'Submit Query'
          )}
        </button>

        {/* Success Message */}
        {submitSuccess && (
          <div className="success-message">
            <CheckCircleOutlined />
            Query processed successfully!
          </div>
        )}
      </form>

      {/* Response Files Section */}
      {responseFiles.length > 0 && (
        <div className="response-files-container">
          <h3>Generated Response Files</h3>
          <div className="response-files-grid">
            {responseFiles.map((file, index) => (
              <div key={index} className="response-file-card">
                <div className="response-file-icon">
                  <FileTextOutlined />
                </div>
                <div className="response-file-details">
                  <h4>{file.title || 'Untitled'}</h4>
                  <div className="response-file-actions">
                    <button 
                      onClick={() => downloadFile(file)}
                      className="download-button"
                    >
                      Download
                    </button>
                    <button 
                      onClick={() => {
                        // Could implement a preview modal here
                        alert(file.content);
                      }}
                      className="preview-button"
                    >
                      Preview
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default FileUploadForm;