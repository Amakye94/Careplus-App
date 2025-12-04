"use strict";

var API_BASE = "http://localhost:8000";

function api(path) {
  var options,
      res,
      _args = arguments;
  return regeneratorRuntime.async(function api$(_context) {
    while (1) {
      switch (_context.prev = _context.next) {
        case 0:
          options = _args.length > 1 && _args[1] !== undefined ? _args[1] : {};
          _context.next = 3;
          return regeneratorRuntime.awrap(fetch(API_BASE + path, {
            method: options.method || "GET",
            headers: {
              "Content-Type": "application/json"
            },
            body: options.body ? JSON.stringify(options.body) : null
          }));

        case 3:
          res = _context.sent;

          if (res.ok) {
            _context.next = 13;
            break;
          }

          _context.t0 = console;
          _context.t1 = res.status;
          _context.next = 9;
          return regeneratorRuntime.awrap(res.text());

        case 9:
          _context.t2 = _context.sent;

          _context.t0.error.call(_context.t0, "API ERROR:", _context.t1, _context.t2);

          alert("Backend error: " + res.status);
          return _context.abrupt("return", []);

        case 13:
          return _context.abrupt("return", res.json());

        case 14:
        case "end":
          return _context.stop();
      }
    }
  });
}