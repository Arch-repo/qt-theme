#!/usr/bin/env python3
"""Pack the Qt Quick control style reproducibly for checksum-pinned delivery."""
from pathlib import Path
import gzip, io, tarfile
ROOT=Path(__file__).resolve().parents[1]
with (ROOT/'palette/quick.tar.gz').open('wb') as output:
 with gzip.GzipFile(fileobj=output,mode='wb',filename='',mtime=0) as compressed:
  with tarfile.open(fileobj=compressed,mode='w',format=tarfile.USTAR_FORMAT) as archive:
   for source in sorted((ROOT/'quick').rglob('*')):
    if not source.is_file():continue
    data=source.read_bytes(); item=tarfile.TarInfo(str(source.relative_to(ROOT/'quick')))
    item.size,item.mode,item.mtime=len(data),0o644,0
    archive.addfile(item,io.BytesIO(data))
