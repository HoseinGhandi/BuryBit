# Copyright (C) 2026 Hosein Ghandi. All Rights Reserved.
# This file is part of BuryBit.
# Licensed under the GNU AGPLv3. See LICENSE file for details.

import os
import zstandard as zstd

class LabyrinthWall:

    def __init__(self, chunk_size: int = 1048576, max_expansion_ratio: int = 150):
        self.chunk_size = chunk_size
        self.max_expansion_ratio = max_expansion_ratio
        
        self.fake_magic_bytes = b"%PDF-1.5\n%\xb5\xb5\xb5\xb5\n"

    def obfuscate_stream(self, input_filepath: str, output_filepath: str) -> None:
        
        cctx = zstd.ZstdCompressor(level=10)
        compressor = cctx.compressobj()

        with open(input_filepath, 'rb') as f_in, open(output_filepath, 'wb') as f_out:
            f_out.write(self.fake_magic_bytes)

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
        header_size = len(self.fake_magic_bytes)

        with open(input_filepath, 'rb') as f_in, open(output_filepath, 'wb') as f_out:
            f_in.read(header_size)

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
                            f"CRITICAL: Zip Bomb payload detected! "
                            f"Expansion ratio ({current_ratio:.1f}x) exceeded."
                        )
                if raw_chunk:
                    f_out.write(raw_chunk)

                    