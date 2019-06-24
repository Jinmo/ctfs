// Copyright 2014 The Chromium Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

'use strict';

(function() {
  var mojomId = 'mojo/public/mojom/base/file.mojom';
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



  function File(values) {
    this.initDefaults_();
    this.initFields_(values);
  }


  File.prototype.initDefaults_ = function() {
    this.fd = null;
    this.async = false;
  };
  File.prototype.initFields_ = function(fields) {
    for(var field in fields) {
        if (this.hasOwnProperty(field))
          this[field] = fields[field];
    }
  };
  File.generate = function(generator_) {
    var generated = new File;
    generated.fd = generator_.generateHandle(false);
    generated.async = generator_.generateBool();
    return generated;
  };

  File.prototype.mutate = function(mutator_) {
    if (mutator_.chooseMutateField()) {
      this.fd = mutator_.mutateHandle(this.fd, false);
    }
    if (mutator_.chooseMutateField()) {
      this.async = mutator_.mutateBool(this.async);
    }
    return this;
  };
  File.prototype.getHandleDeps = function() {
    var handles = [];
    if (this.fd !== null) {
      Array.prototype.push.apply(handles, ["None"]);
    }
    return handles;
  };

  File.prototype.setHandles = function() {
    this.setHandlesInternal_(arguments, 0);
  };
  File.prototype.setHandlesInternal_ = function(handles, idx) {
    this.fd = handles[idx++];;
    return idx;
  };

  File.validate = function(messageValidator, offset) {
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


    // validate File.fd
    err = messageValidator.validateHandle(offset + codec.kStructHeaderSize + 0, false)
    if (err !== validator.validationError.NONE)
        return err;


    return validator.validationError.NONE;
  };

  File.encodedSize = codec.kStructHeaderSize + 8;

  File.decode = function(decoder) {
    var packed;
    var val = new File();
    var numberOfBytes = decoder.readUint32();
    var version = decoder.readUint32();
    val.fd = decoder.decodeStruct(codec.Handle);
    packed = decoder.readUint8();
    val.async = (packed >> 0) & 1 ? true : false;
    decoder.skip(1);
    decoder.skip(1);
    decoder.skip(1);
    return val;
  };

  File.encode = function(encoder, val) {
    var packed;
    encoder.writeUint32(File.encodedSize);
    encoder.writeUint32(0);
    encoder.encodeStruct(codec.Handle, val.fd);
    packed = 0;
    packed |= (val.async & 1) << 0
    encoder.writeUint8(packed);
    encoder.skip(1);
    encoder.skip(1);
    encoder.skip(1);
  };
  exports.File = File;
})();