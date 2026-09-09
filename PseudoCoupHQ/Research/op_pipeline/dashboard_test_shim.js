/* dashboard_test_shim.js -- a TEST RIG ONLY.  Not part of the dashboard.
 *
 * The live page reads the folder through the File System Access API.  That
 * API's folder dialog belongs to the operating system and no automation
 * here can click it, so the live page cannot be driven end to end by a
 * script.  This shim exists only so the loader can be MEASURED in a real
 * browser: it dresses ranged http fetches (dashboard_test_server.py) as
 * directory handles with the same four calls the loader makes --
 * getFileHandle, getFile, slice/text and values.
 *
 * dashboard_loader.js is used UNCHANGED against it; nothing in the
 * dashboard knows this file exists.
 */
var TestShim = (function () {
  "use strict";

  function fileLike(url, size) {
    return {
      size: size,
      slice: function (a, b) {
        return {
          text: function () {
            var headers = { Range: "bytes=" + a + "-" + (b - 1) };
            return fetch(url, { headers: headers }).then(function (r) {
              return r.text();
            });
          }
        };
      },
      text: function () {
        return fetch(url).then(function (r) {
          return r.text();
        });
      }
    };
  }

  function dirHandle(base) {
    return {
      name: base,
      getFileHandle: function (name) {
        var url = base + "/" + name;
        return fetch(url, { method: "HEAD" }).then(function (r) {
          if (!r.ok) {
            throw new Error("no such file: " + name);
          }
          var n = Number(r.headers.get("Content-Length") || 0);
          return { getFile: function () { return Promise.resolve(fileLike(url, n)); } };
        });
      },
      getDirectoryHandle: function (name) {
        var url = base + "/" + name + "/";
        return fetch(url).then(function (r) {
          if (!r.ok) {
            throw new Error("no such directory: " + name);
          }
          return dirHandle(base + "/" + name);
        });
      },
      values: function () {
        var pending = fetch(base + "/").then(function (r) {
          return r.text();
        }).then(function (html) {
          var out = [];
          var re = /href="([^"?/]+)"/g;
          var m = re.exec(html);
          while (m) {
            out.push({ kind: "file", name: decodeURIComponent(m[1]) });
            m = re.exec(html);
          }
          return out;
        });
        return {
          [Symbol.asyncIterator]: function () {
            var i = 0;
            var list = null;
            return {
              next: function () {
                return pending.then(function (l) {
                  list = l;
                  if (i >= list.length) {
                    return { done: true };
                  }
                  i += 1;
                  return { done: false, value: list[i - 1] };
                });
              }
            };
          }
        };
      }
    };
  }

  return { dirHandle: dirHandle };
}());
