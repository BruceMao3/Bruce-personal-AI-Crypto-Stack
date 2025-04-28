const express = require('express');
const bodyParser = require('body-parser');
const app = express();
const port = 3000;

// 中间件
app.use(bodyParser.json());
app.use(express.static('public'));

// 只允许本地访问的中间件
app.use((req, res, next) => {
  const ip = req.ip || req.connection.remoteAddress;
  if (ip === '::1' || ip === '127.0.0.1' || ip.includes('::ffff:127.0.0.1')) {
    next();
  } else {
    res.status(403).send('只允许本地访问');
  }
});

// 存储收到的卡片数据
let cards = [];

// 接收POST请求的路由
app.post('/api/card', (req, res) => {
  const { platform, title, content } = req.body;
  
  if (!platform || !title) {
    return res.status(400).json({ error: '缺少必要字段' });
  }
  
  const id = Date.now(); // 使用时间戳作为唯一ID
  const newCard = { id, platform, title, content, time: new Date().toLocaleString() };
  cards.push(newCard);
  
  res.json({ success: true, id });
});

// 获取所有卡片
app.get('/api/cards', (req, res) => {
  res.json(cards);
});

// 删除卡片
app.delete('/api/card/:id', (req, res) => {
  const id = parseInt(req.params.id);
  const initialLength = cards.length;
  cards = cards.filter(card => card.id !== id);
  
  if (cards.length < initialLength) {
    res.json({ success: true });
  } else {
    res.status(404).json({ error: '卡片未找到' });
  }
});

app.listen(port, () => {
  console.log(`服务器运行在 http://localhost:${port}`);
}); 