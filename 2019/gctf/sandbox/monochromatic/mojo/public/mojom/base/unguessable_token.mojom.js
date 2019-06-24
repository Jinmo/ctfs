// Copyright 2014 The Chromium Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

'use strict';

(function() {
  var mojomId = 'mojo/public/mojom/base/unguessable_token.mojom';
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



  function UnguessableToken(values) {
    this.initDefaults_();
    this.initFields_(values);
  }


  UnguessableToken.prototype.initDefaults_ = function() {
    this.high = 0;
    this.low = 0;
  };
  UnguessableToken.prototype.initFields_ = function(fields) {
    for(var field in fields) {
        if (this.hasOwnProperty(field))
          this[field] = fields[field];
    }
  };
  UnguessableToken.generate = function(generator_) {
    var generated = new UnguessableToken;
    generated.high = generator_.generateUint64();
    generated.low = generator_.generateUint64();
    return generated;
  };

  UnguessableToken.prototype.mutate = function(mutator_) {
    if (mutator_.chooseMutateField()) {
      this.high = mutator_.mutateUint64(this.high);
    }
    if (mutator_.chooseMutateField()) {
      this.low = mutator_.mutateUint64(this.low);
    }
    return this;
  };
  UnguessableToken.prototype.getHandleDeps = function() {
    var handles = [];
    return handles;
  };

  UnguessableToken.prototype.setHandles = function() {
    this.setHandlesInternal_(arguments, 0);
  };
  UnguessableToken.prototype.setHandlesInternal_ = function(handles, idx) {
    return idx;
  };

  UnguessableToken.validate = function(messageValidator, offset) {
    var err;
    err = messageValidator.validateStructHeader(offset, codec.kStructHeaderSize);
    if (err !== validator.validationError.NONE)
        return err;

    var kVersionSizes = [
      {version: 0, numBytes: 24}
    ];
    err = messageValidator.validateStructVersion(offset, kVersionSizes);
    if (err !== validator.validationError.NONE)
        return err;



    return validator.validationError.NONE;
  };

  UnguessableToken.encodedSize = codec.kStructHeaderSize + 16;

  UnguessableToken.decode = function(decoder) {
    var packed;
    var val = new UnguessableToken();
    var numberOfBytes = decoder.readUint32();
    var version = decoder.readUint32();
    val.high = decoder.decodeStruct(codec.Uint64);
    val.low = decoder.decodeStruct(codec.Uint64);
    return val;
  };

  UnguessableToken.encode = function(encoder, val) {
    var packed;
    encoder.writeUint32(UnguessableToken.encodedSize);
    encoder.writeUint32(0);
    encoder.encodeStruct(codec.Uint64, val.high);
    encoder.encodeStruct(codec.Uint64, val.low);
  };
  exports.UnguessableToken = UnguessableToken;
})();