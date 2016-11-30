Steps:
  1. Compress the data you're going to upload.
  2. Use the reed solomon error correction algorithm on the whole amount of compressed data, using highest level of correction
  3. split data into about 4mb chunks
  4. grab md5sum of chunk, place md5 at beginning of data followed by 4 characters of hexadecimal for an id field, and turn the data into an image.
