import { NextApiRequest, NextApiResponse } from 'next';
import formidable from 'formidable';
import fs from 'fs';
import path from 'path';

export const config = {
  api: {
    bodyParser: false,
  },
};

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    // 配置上传目录
    const uploadDir = path.join(process.cwd(), '../../data/uploads');
    
    // 确保上传目录存在
    if (!fs.existsSync(uploadDir)) {
      fs.mkdirSync(uploadDir, { recursive: true });
    }

    const form = formidable({
      uploadDir,
      keepExtensions: true,
      maxFileSize: 100 * 1024 * 1024, // 100MB
      filename: (name, ext, part, form) => {
        // 保持原文件名
        return part.originalFilename || `file_${Date.now()}${ext}`;
      }
    });

    const [fields, files] = await form.parse(req);
    const file = Array.isArray(files.file) ? files.file[0] : files.file;

    if (!file) {
      return res.status(400).json({ error: '没有文件上传' });
    }

    // 返回完整的文件路径
    const filePath = file.filepath;
    const fileName = file.originalFilename || path.basename(filePath);
    
    console.log(`文件上传成功: ${fileName} -> ${filePath}`);
    
    res.status(200).json({
      success: true,
      fileName: fileName,
      filePath: filePath,
      size: file.size
    });

  } catch (error) {
    console.error('文件上传错误:', error);
    res.status(500).json({ 
      error: '文件上传失败',
      details: error.message 
    });
  }
}