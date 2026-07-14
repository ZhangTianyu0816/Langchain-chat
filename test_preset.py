# test_preset.py
import sys
import asyncio

# 将 src 物理注入解释器检索路径
sys.path.insert(0, 'src')

from models.schemas import Preset
from storage.sqlite_backend import SQLiteBackend

async def t():
    # 初始化本地 SQLite 沙箱隔离数据库
    b = SQLiteBackend('data/sqlite/_test.db')
    
    try:
        await b.initialize()

        # 执行持久化数据注入
        p = await b.save_preset(Preset(id=0, user_id=None, name='测试', system_prompt='你'))
        print('保存返回 id:', p.id)

        # 物理打捞 presets 表的记录总数进行数据完整性验证
        # 查询 presets 表的记录总数，验证数据完整性
        import aiosqlite
        async with b._conn.execute('SELECT COUNT(*) FROM presets') as c:
            r = await c.fetchone()
        print('presets 表记录数:', r[0])
    finally:
	    # 优雅关闭物理连接流：确保无论是否报错，都关闭 SQLite 连接
    	await b.close()

if __name__ == '__main__':
    asyncio.run(t())