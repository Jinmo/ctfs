// Copyright 2014 The Chromium Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

'use strict';

(function() {
  var mojomId = 'mojo/public/mojom/base/file_path.mojom';
  if (mojo.internal.isMojomLoaded(mojomId)) {
    console.warn('The following mojom is loaded multiple times: ' + mojomId);
    return;
  }
  mojo.internal.markMojomLoaded(mojomId);
  var bindings = mojo;
  var associatedBindings = mojo;
  var codec = mojo.internal;
  var validator = mojo.internal;

  var exports = mojo.internal.exposeNamespace('mojoBase.mojom');



  function FilePath(values) {
    this.initDefaults_();
    this.initFields_(values);
  }


  FilePath.prototype.initDefaults_ = function() {
    this.path = null;
  };
  FilePath.prototype.initFields_ = function(fields) {
    for(var field in fields) {
        if (this.hasOwnProperty(field))
          this[field] = fields[field];
    }
  };
  FilePath.generate = function(generator_) {
    var generated = new FilePath;
    generated.path = generator_.generateString(false);
    return generated;
  };

  FilePath.prototype.mutate = function(mutator_) {
    if (mutator_.chooseMutateField()) {
      this.path = mutator_.mutateString(this.path, false);
    }
    return this;
  };
  FilePath.prototype.getHandleDeps = function() {
    var handles = [];
    return handles;
  };

  FilePath.prototype.setHandles = function() {
    this.setHandlesInternal_(arguments, 0);
  };
  FilePath.prototype.setHandlesInternal_ = function(handles, idx) {
    return idx;
  };

  FilePath.validate = function(messageValidator, offset) {
    var err;
    err = messageValidator.validateStructHeader(offset, codec.kStructHeaderSize);
    if (err !== validator.validationError.NONE)
        return err;

    var kVersionSizes = [
      {version: 0, numBytes: 16}
    ];
    err = messageValidator.validateStructVersion(offset, kVersionSizes);
    if (err !== validator.validationError.NONE)
        return err;


    // validate FilePath.path
    err = messageValidator.validateStringPointer(offset + codec.kStructHeaderSize + 0, false)
    if (err !== validator.validationError.NONE)
        return err;

    return validator.validationError.NONE;
  };

  FilePath.encodedSize = codec.kStructHeaderSize + 8;

  FilePath.decode = function(decoder) {
    var packed;
    var val = new FilePath();
    var numberOfBytes = decoder.readUint32();
    var version = decoder.readUint32();
    val.path = decoder.decodeStruct(codec.String);
    return val;
  };

  FilePath.encode = function(encoder, val) {
    var packed;
    encoder.writeUint32(FilePath.encodedSize);
    encoder.writeUint32(0);
    encoder.encodeStruct(codec.String, val.path);
  };
  exports.FilePath = FilePath;
})();