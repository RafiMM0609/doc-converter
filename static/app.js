// API Configuration
const API_BASE_URL = 'http://localhost:8000/api';

// DOM Elements
const convertUploadArea = document.getElementById('convertUploadArea');
const convertFileInput = document.getElementById('convertFileInput');
const convertFileInfo = document.getElementById('convertFileInfo');
const convertBtn = document.getElementById('convertBtn');
const convertProgress = document.getElementById('convertProgress');
const convertProgressBar = document.getElementById('convertProgressBar');
const convertProgressText = document.getElementById('convertProgressText');
const convertResult = document.getElementById('convertResult');
const convertPreview = document.getElementById('convertPreview');

const mergeUploadArea = document.getElementById('mergeUploadArea');
const mergeFileInput = document.getElementById('mergeFileInput');
const mergeFileInfo = document.getElementById('mergeFileInfo');
const mergeBtn = document.getElementById('mergeBtn');
const mergeProgress = document.getElementById('mergeProgress');
const mergeProgressBar = document.getElementById('mergeProgressBar');
const mergeProgressText = document.getElementById('mergeProgressText');
const mergeResult = document.getElementById('mergeResult');

const errorNotification = document.getElementById('errorNotification');
const successNotification = document.getElementById('successNotification');

// State variables
let convertSelectedFile = null;
let mergeSelectedFiles = [];
let convertResultBlob = null;
let mergeResultBlob = null;

// ========================================
// Tab Navigation
// ========================================

document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        const tabName = btn.getAttribute('data-tab');
        
        document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
        document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));
        
        btn.classList.add('active');
        document.getElementById(tabName).classList.add('active');
    });
});

// ========================================
// Convert PDF to JPG - File Handling
// ========================================

convertUploadArea.addEventListener('click', () => convertFileInput.click());

convertUploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    convertUploadArea.classList.add('dragover');
});

convertUploadArea.addEventListener('dragleave', () => {
    convertUploadArea.classList.remove('dragover');
});

convertUploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    convertUploadArea.classList.remove('dragover');
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        handleConvertFileSelect(files[0]);
    }
});

convertFileInput.addEventListener('change', (e) => {
    if (e.target.files.length > 0) {
        handleConvertFileSelect(e.target.files[0]);
    }
});

function handleConvertFileSelect(file) {
    if (!file.type.includes('pdf')) {
        showError('Please select a PDF file');
        return;
    }
    
    if (file.size > 10 * 1024 * 1024) {
        showError('File size exceeds 10 MB limit');
        return;
    }
    
    convertSelectedFile = file;
    displayConvertFile();
}

function displayConvertFile() {
    if (!convertSelectedFile) return;
    
    const fileSize = formatFileSize(convertSelectedFile.size);
    document.getElementById('convertFileName').textContent = convertSelectedFile.name;
    document.getElementById('convertFileSize').textContent = fileSize;
    
    convertFileInfo.style.display = 'block';
    convertBtn.style.display = 'block';
    convertUploadArea.style.opacity = '0.5';
}

function clearConvertFile() {
    convertSelectedFile = null;
    convertFileInput.value = '';
    convertFileInfo.style.display = 'none';
    convertBtn.style.display = 'none';
    convertUploadArea.style.opacity = '1';
}

// ========================================
// Merge PDFs - File Handling
// ========================================

mergeUploadArea.addEventListener('click', () => mergeFileInput.click());

mergeUploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    mergeUploadArea.classList.add('dragover');
});

mergeUploadArea.addEventListener('dragleave', () => {
    mergeUploadArea.classList.remove('dragover');
});

mergeUploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    mergeUploadArea.classList.remove('dragover');
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        handleMergeFilesSelect(files);
    }
});

mergeFileInput.addEventListener('change', (e) => {
    if (e.target.files.length > 0) {
        handleMergeFilesSelect(e.target.files);
    }
});

function handleMergeFilesSelect(files) {
    const newFiles = Array.from(files);
    
    for (const file of newFiles) {
        if (!file.type.includes('pdf')) {
            showError('All files must be PDF files');
            return;
        }
        
        if (file.size > 10 * 1024 * 1024) {
            showError(`File ${file.name} exceeds 10 MB limit`);
            return;
        }
    }
    
    mergeSelectedFiles = [...mergeSelectedFiles, ...newFiles];
    displayMergeFiles();
}

function displayMergeFiles() {
    if (mergeSelectedFiles.length === 0) {
        mergeFileInfo.style.display = 'none';
        mergeBtn.style.display = 'none';
        mergeUploadArea.style.opacity = '1';
        return;
    }
    
    const fileList = document.getElementById('mergeFilesList');
    fileList.innerHTML = '';
    
    mergeSelectedFiles.forEach((file, index) => {
        const li = document.createElement('li');
        const fileSize = formatFileSize(file.size);
        li.innerHTML = `
            <div class="file-info">
                <div class="file-name">${file.name}</div>
                <div class="file-size">${fileSize}</div>
            </div>
            <button type="button" class="btn-remove" onclick="removeMergeFile(${index})">✕</button>
        `;
        fileList.appendChild(li);
    });
    
    document.getElementById('mergeFileCount').textContent = mergeSelectedFiles.length;
    
    mergeFileInfo.style.display = 'block';
    
    if (mergeSelectedFiles.length >= 2) {
        mergeBtn.style.display = 'block';
        mergeUploadArea.style.opacity = '0.5';
    } else {
        mergeBtn.style.display = 'none';
        mergeUploadArea.style.opacity = '1';
    }
}

function removeMergeFile(index) {
    mergeSelectedFiles.splice(index, 1);
    displayMergeFiles();
}

function clearMergeFiles() {
    mergeSelectedFiles = [];
    mergeFileInput.value = '';
    displayMergeFiles();
}

// ========================================
// Convert PDF to JPG Function
// ========================================

async function convertPdf() {
    if (!convertSelectedFile) {
        showError('Please select a PDF file');
        return;
    }
    
    convertBtn.disabled = true;
    convertProgress.style.display = 'block';
    convertResult.style.display = 'none';
    
    const formData = new FormData();
    formData.append('file', convertSelectedFile);
    
    try {
        const response = await fetch(`${API_BASE_URL}/convert-pdf-to-jpg`, {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Conversion failed');
        }
        
        convertResultBlob = await response.blob();
        displayConvertResult();
        showSuccess('PDF converted to JPG successfully!');
        
    } catch (error) {
        showError(error.message || 'Failed to convert PDF');
        convertProgress.style.display = 'none';
        convertBtn.disabled = false;
    }
}

function displayConvertResult() {
    const url = URL.createObjectURL(convertResultBlob);
    convertPreview.src = url;
    
    const fileSize = formatFileSize(convertResultBlob.size);
    document.getElementById('convertResultInfo').textContent = 
        `File size: ${fileSize} • Format: JPG`;
    
    convertProgress.style.display = 'none';
    convertResult.style.display = 'block';
    convertBtn.disabled = false;
}

function downloadConvertResult() {
    if (!convertResultBlob) return;
    
    const url = URL.createObjectURL(convertResultBlob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `converted-${Date.now()}.jpg`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}

function resetConvertTab() {
    clearConvertFile();
    convertProgress.style.display = 'none';
    convertResult.style.display = 'none';
    convertResultBlob = null;
}

// ========================================
// Merge PDFs Function
// ========================================

async function mergePdfs() {
    if (mergeSelectedFiles.length < 2) {
        showError('Please select at least 2 PDF files');
        return;
    }
    
    mergeBtn.disabled = true;
    mergeProgress.style.display = 'block';
    mergeResult.style.display = 'none';
    
    const formData = new FormData();
    mergeSelectedFiles.forEach(file => {
        formData.append('files', file);
    });
    
    try {
        const response = await fetch(`${API_BASE_URL}/merge-pdfs`, {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Merge failed');
        }
        
        mergeResultBlob = await response.blob();
        displayMergeResult();
        showSuccess(`Successfully merged ${mergeSelectedFiles.length} PDF files!`);
        
    } catch (error) {
        showError(error.message || 'Failed to merge PDFs');
        mergeProgress.style.display = 'none';
        mergeBtn.disabled = false;
    }
}

function displayMergeResult() {
    const fileSize = formatFileSize(mergeResultBlob.size);
    document.getElementById('mergeResultInfo').textContent = 
        `Merged ${mergeSelectedFiles.length} PDF files • Size: ${fileSize}`;
    
    mergeProgress.style.display = 'none';
    mergeResult.style.display = 'block';
    mergeBtn.disabled = false;
}

function downloadMergeResult() {
    if (!mergeResultBlob) return;
    
    const url = URL.createObjectURL(mergeResultBlob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `merged-${Date.now()}.pdf`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}

function resetMergeTab() {
    clearMergeFiles();
    mergeProgress.style.display = 'none';
    mergeResult.style.display = 'none';
    mergeResultBlob = null;
}

// ========================================
// Notifications
// ========================================

function showError(message) {
    document.getElementById('errorMessage').textContent = message;
    errorNotification.style.display = 'flex';
    
    setTimeout(() => {
        errorNotification.style.display = 'none';
    }, 5000);
}

function showSuccess(message) {
    document.getElementById('successMessage').textContent = message;
    successNotification.style.display = 'flex';
    
    setTimeout(() => {
        successNotification.style.display = 'none';
    }, 5000);
}

function closeNotification() {
    errorNotification.style.display = 'none';
    successNotification.style.display = 'none';
}

// ========================================
// Utility Functions
// ========================================

function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    
    return Math.round((bytes / Math.pow(k, i)) * 100) / 100 + ' ' + sizes[i];
}

function showApiDocs() {
    window.open('http://localhost:8000/docs', '_blank');
}

// ========================================
// Initialize
// ========================================

document.addEventListener('DOMContentLoaded', () => {
    console.log('PDF Converter UI initialized');
});
