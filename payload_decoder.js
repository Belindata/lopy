function Decoder(bytes, port) {
  // Decode an uplink message from a buffer
  // (array) of bytes to an object of fields.
  var decoded = {};

  // Decode bytes to int
  decoded.x = (((bytes[1] << 8) | bytes[0]) - 32768) / 10000;
  decoded.y = (((bytes[3] << 8) | bytes[2]) - 32768) / 10000;
  decoded.z = (((bytes[5] << 8) | bytes[4]) - 32768) / 10000;

  return decoded;
}
