/**
 * end facing direction of robot for each position
 * 
 * 0: up
 * 1: up
 * 2: up
 * 3: left 
 * 4: right
 * 5: up
 * 6: up
 * 7: up
 */

const F = 1;
const B = 2;
const L = 3;
const R = 4;

exports.paths = {
    0: {
      1: [B, R, F, L, F],
      2: [B, R, F, F, L, F],
      3: [B, L, F],
      4: [B, R, F, F, F],
      5: [B],
      6: [B, R, F, L],
      7: [B, R, F, F, L]
    },
    1: {
      0: [B, L, F, R, F],
      2: [B, R, F, L, F],
      3: [B, L, F, F],
      4: [B, R, F, F],
      5: [B, L, F, R],
      6: [B],
      7: [B, R, F, L]
    },
    2: {
      0: [B, L, F, F, R, F],
      1: [B, L, F, R, F],
        // 1: [B, F, R, F, R, F],
      3: [B, L, F, F, F],
      4: [B, R, F],
      5: [B, L, F, F, R],
      6: [B, L, F, R],
      7: [B]
    },
    3: {
      0: [B, R, F],
      1: [B, B, R, F],
      2: [B, B, B, R, F],
      4: [B, B, B, B, R, R],
      5: [B, R],
      6: [B, B, R],
      7: [B, B, B, R]
    },
    4: {
      0: [B, B, B, L, F],
      1: [B, B, L, F],
      2: [B, L, F],
      3: [B, B, B, B, L, L],
      5: [B, B, B, L],
      6: [B, B, L],
      7: [B, L]
    },
    5: {
      0: [F],
      1: [R, F, L, F],
      2: [R, F, F, L, F],
      3: [L, F],
      4: [R, F, F, F],
      6: [R, F, L],
      7: [R, F, F, L]
    },
    6: {
      0: [L, F, R, F],
      1: [F],
      2: [R, F, L, F],
      3: [L, F, F],
      4: [R, F, F],
      5: [L, F, R],
      7: [R, F, L]
    },
    7: {
      0: [L, F, F, R, F],
      1: [L, F, R, F],
      2: [F],
      3: [L, F, F, F],
      4: [R, F],
      5: [L, F, F, R],
      6: [L, F, R]
    },
    8: {
      0: [F, L, F, R, F],
      1: [F, F],
      2: [F, R, F, L, F],
      3: [F, L, F, F],
      4: [F, R, F, F],
      5: [F, L, F, R],
      7: [F, R, F, L]
    },
  }