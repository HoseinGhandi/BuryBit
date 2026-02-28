# Copyright (C) 2026 Hosein Ghandi. All Rights Reserved.
# This file is part of BuryBit.
# Licensed under the GNU AGPLv3. See LICENSE file for details.

import os
import random
import zstandard as zstd

class LabyrinthWall:
   

    def __init__(self, chunk_size: int = 1048576, max_expansion_ratio: int = 150):
        self.chunk_size = chunk_size
        self.max_expansion_ratio = max_expansion_ratio
        
        self.magic_pool = [
            b"%PDF-1.7\n%\xb5\xb5\xb5\xb5\n",                  # Adobe PDF
            b"\xFF\xD8\xFF\xE0\x00\x10JFIF",                   # JPEG Image
            b"\x89PNG\r\n\x1a\n",                              # PNG Image
            b"PK\x03\x04",                                     # ZIP / DOCX / XLSX
            b"\x00\x00\x00\x18ftypmp42",                       # MP4 Video
            b"ID3\x04\x00\x00\x00",                            # MP3 Audio
            b"8BPS\x00\x01\x00\x00\x00\x00\x00\x00\x00\x03",   # Adobe PSD
            b"\xD0\xCF\x11\xE0\xA1\xB1\x1A\xE1",               # MS Office Legacy
            b"GIF89a",                                         # GIF Animation
            b"Rar!\x1A\x07\x00"                                # RAR Archive
        ]
        
        self.zstd_magic = b'\x28\xb5\x2f\xfd'

    def obfuscate_stream(self, input_filepath: str, output_filepath: str) -> None:
        
        cctx = zstd.ZstdCompressor(level=10)
        compressor = cctx.compressobj()

        chosen_magic = random.choice(self.magic_pool)

        with open(input_filepath, 'rb') as f_in, open(output_filepath, 'wb') as f_out:
            f_out.write(chosen_magic)

            while True:
                raw_chunk = f_in.read(self.chunk_size)
                if not raw_chunk:
                    break
                compressed_chunk = compressor.compress(raw_chunk)
                if compressed_chunk:
                    f_out.write(compressed_chunk)

            final_chunk = compressor.flush()
            if final_chunk:
                f_out.write(final_chunk)

    def reveal_stream(self, input_filepath: str, output_filepath: str) -> None:
        
        dctx = zstd.ZstdDecompressor()
        decompressor = dctx.decompressobj()

        total_compressed = 0
        total_decompressed = 0

        with open(input_filepath, 'rb') as f_in, open(output_filepath, 'wb') as f_out:
            scan_buffer = f_in.read(128)
            
            start_index = scan_buffer.find(self.zstd_magic)
            if start_index == -1:
                raise ValueError("🚨 CRITICAL: File is corrupted or not obfuscated by BuryBit. Zstandard signature missing.")
            
            f_in.seek(start_index)

            while True:
                compressed_chunk = f_in.read(self.chunk_size)
                if not compressed_chunk:
                    break
                
                total_compressed += len(compressed_chunk)
                raw_chunk = decompressor.decompress(compressed_chunk)
                total_decompressed += len(raw_chunk)

                if total_compressed > 1048576:
                    current_ratio = total_decompressed / total_compressed
                    if current_ratio > self.max_expansion_ratio:
                        f_out.close()
                        os.remove(output_filepath)
                        raise PermissionError(
                            f"🚨 CRITICAL: Zip Bomb payload detected! Expansion ratio exceeded."
                        )

                if raw_chunk:
                    f_out.write(raw_chunk)