'use client';

import React, { useRef, useState, useCallback } from 'react';
import { IconUpload, IconFile, IconX, IconCheck } from '@tabler/icons-react';

interface FileUploadProps {
  onFileUpload?: (file: File, data: any) => void;
  className?: string;
}

export const DataFileUpload: React.FC<FileUploadProps> = ({ 
  onFileUpload, 
  className = '' 
}) => {
  const [isDragActive, setIsDragActive] = useState(false);
  const [uploadedFile, setUploadedFile] = useState<File | null>(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [uploadStatus, setUploadStatus] = useState<'idle' | 'success' | 'error'>('idle');
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleDragEnter = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragActive(true);
  }, []);

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragActive(false);
  }, []);

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
  }, []);

  const processFile = async (file: File) => {
    setIsProcessing(true);
    setUploadStatus('idle');

    try {
      // 验证文件类型
      const allowedTypes = [
        'text/csv',
        'application/vnd.ms-excel',
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
      ];
      
      if (!allowedTypes.includes(file.type) && 
          !['.csv', '.xlsx', '.xls'].some(ext => file.name.toLowerCase().endsWith(ext))) {
        throw new Error('仅支持 CSV、Excel (.xlsx/.xls) 文件格式');
      }

      // 验证文件大小 (100MB 限制)
      if (file.size > 100 * 1024 * 1024) {
        throw new Error('文件大小不能超过 100MB');
      }

      // 读取文件内容
      const fileData = await new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = (e) => resolve(e.target?.result);
        reader.onerror = () => reject(new Error('文件读取失败'));
        reader.readAsArrayBuffer(file);
      });

      const fileInfo = {
        name: file.name,
        size: file.size,
        type: file.type,
        lastModified: file.lastModified,
        data: fileData
      };

      setUploadedFile(file);
      setUploadStatus('success');
      
      // 调用上传回调
      if (onFileUpload) {
        onFileUpload(file, fileInfo);
      }

    } catch (error) {
      console.error('文件处理失败:', error);
      setUploadStatus('error');
      alert(error.message || '文件处理失败，请重试');
    } finally {
      setIsProcessing(false);
    }
  };

  const handleDrop = useCallback(async (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragActive(false);

    const files = Array.from(e.dataTransfer.files);
    if (files.length > 0) {
      await processFile(files[0]);
    }
  }, []);

  const handleFileInputChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (files && files.length > 0) {
      await processFile(files[0]);
    }
  };

  const handleClick = () => {
    fileInputRef.current?.click();
  };

  const handleRemoveFile = (e: React.MouseEvent) => {
    e.stopPropagation();
    setUploadedFile(null);
    setUploadStatus('idle');
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  const getStatusIcon = () => {
    if (isProcessing) {
      return <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-blue-600"></div>;
    }
    if (uploadStatus === 'success') {
      return <IconCheck size={24} className="text-green-600" />;
    }
    if (uploadStatus === 'error') {
      return <IconX size={24} className="text-red-600" />;
    }
    return <IconUpload size={24} className="text-blue-600" />;
  };

  const getBorderColor = () => {
    if (isDragActive) return 'border-blue-500 bg-blue-50 dark:bg-blue-900/20';
    if (uploadStatus === 'success') return 'border-green-500 bg-green-50 dark:bg-green-900/20';
    if (uploadStatus === 'error') return 'border-red-500 bg-red-50 dark:bg-red-900/20';
    return 'border-gray-300 dark:border-gray-600 hover:border-blue-400 dark:hover:border-blue-500';
  };

  return (
    <div className={`w-full ${className}`}>
      <div
        onClick={handleClick}
        onDragEnter={handleDragEnter}
        onDragLeave={handleDragLeave}
        onDragOver={handleDragOver}
        onDrop={handleDrop}
        className={`
          relative border-2 border-dashed rounded-lg p-6 cursor-pointer
          transition-all duration-200 ease-in-out
          ${getBorderColor()}
          ${isProcessing ? 'cursor-wait' : 'cursor-pointer'}
        `}
      >
        <input
          ref={fileInputRef}
          type="file"
          accept=".csv,.xlsx,.xls,application/vnd.ms-excel,application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
          onChange={handleFileInputChange}
          className="hidden"
          disabled={isProcessing}
        />

        <div className="flex flex-col items-center justify-center space-y-4">
          {uploadedFile ? (
            <>
              <div className="flex items-center space-x-3">
                <IconFile size={32} className="text-blue-600" />
                <div className="text-left">
                  <p className="font-medium text-gray-900 dark:text-white">{uploadedFile.name}</p>
                  <p className="text-sm text-gray-500 dark:text-gray-400">
                    {(uploadedFile.size / 1024 / 1024).toFixed(2)} MB
                  </p>
                </div>
                {getStatusIcon()}
                {!isProcessing && (
                  <button
                    onClick={handleRemoveFile}
                    className="p-1 rounded-full hover:bg-gray-200 dark:hover:bg-gray-700 transition-colors"
                  >
                    <IconX size={20} className="text-gray-500" />
                  </button>
                )}
              </div>
              {uploadStatus === 'success' && (
                <p className="text-sm text-green-600 dark:text-green-400">
                  ✅ 文件上传成功！可以开始分析了
                </p>
              )}
            </>
          ) : (
            <>
              {getStatusIcon()}
              <div className="text-center">
                <p className="text-lg font-medium text-gray-900 dark:text-white mb-2">
                  📊 上传数据文件
                </p>
                <p className="text-sm text-gray-600 dark:text-gray-400 mb-2">
                  拖拽文件到此处或点击选择文件
                </p>
                <p className="text-xs text-gray-500 dark:text-gray-500">
                  支持 CSV, Excel (.xlsx/.xls) 格式，最大 100MB
                </p>
              </div>
            </>
          )}
        </div>

        {isDragActive && (
          <div className="absolute inset-0 bg-blue-100 dark:bg-blue-900/30 rounded-lg flex items-center justify-center">
            <p className="text-blue-700 dark:text-blue-300 font-medium">
              释放文件开始上传
            </p>
          </div>
        )}
      </div>
    </div>
  );
};