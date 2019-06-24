// Copyright 2014 The Chromium Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

'use strict';

(function() {
  var mojomId = 'mojo/public/mojom/base/time.mojom';
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



  function Time(values) {
    this.initDefaults_();
    this.initFields_(values);
  }


  Time.prototype.initDefaults_ = function() {
    this.internalValue = 0;
  };
  Time.prototype.initFields_ = function(fields) {
    for(var field in fields) {
        if (this.hasOwnProperty(field))
          this[field] = fields[field];
    }
  };
  Time.generate = function(generator_) {
    var generated = new Time;
    generated.internalValue = generator_.generateInt64();
    return generated;
  };

  Time.prototype.mutate = function(mutator_) {
    if (mutator_.chooseMutateField()) {
      this.internalValue = mutator_.mutateInt64(this.internalValue);
    }
    return this;
  };
  Time.prototype.getHandleDeps = function() {
    var handles = [];
    return handles;
  };

  Time.prototype.setHandles = function() {
    this.setHandlesInternal_(arguments, 0);
  };
  Time.prototype.setHandlesInternal_ = function(handles, idx) {
    return idx;
  };

  Time.validate = function(messageValidator, offset) {
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


    return validator.validationError.NONE;
  };

  Time.encodedSize = codec.kStructHeaderSize + 8;

  Time.decode = function(decoder) {
    var packed;
    var val = new Time();
    var numberOfBytes = decoder.readUint32();
    var version = decoder.readUint32();
    val.internalValue = decoder.decodeStruct(codec.Int64);
    return val;
  };

  Time.encode = function(encoder, val) {
    var packed;
    encoder.writeUint32(Time.encodedSize);
    encoder.writeUint32(0);
    encoder.encodeStruct(codec.Int64, val.internalValue);
  };
  function TimeDelta(values) {
    this.initDefaults_();
    this.initFields_(values);
  }


  TimeDelta.prototype.initDefaults_ = function() {
    this.microseconds = 0;
  };
  TimeDelta.prototype.initFields_ = function(fields) {
    for(var field in fields) {
        if (this.hasOwnProperty(field))
          this[field] = fields[field];
    }
  };
  TimeDelta.generate = function(generator_) {
    var generated = new TimeDelta;
    generated.microseconds = generator_.generateInt64();
    return generated;
  };

  TimeDelta.prototype.mutate = function(mutator_) {
    if (mutator_.chooseMutateField()) {
      this.microseconds = mutator_.mutateInt64(this.microseconds);
    }
    return this;
  };
  TimeDelta.prototype.getHandleDeps = function() {
    var handles = [];
    return handles;
  };

  TimeDelta.prototype.setHandles = function() {
    this.setHandlesInternal_(arguments, 0);
  };
  TimeDelta.prototype.setHandlesInternal_ = function(handles, idx) {
    return idx;
  };

  TimeDelta.validate = function(messageValidator, offset) {
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


    return validator.validationError.NONE;
  };

  TimeDelta.encodedSize = codec.kStructHeaderSize + 8;

  TimeDelta.decode = function(decoder) {
    var packed;
    var val = new TimeDelta();
    var numberOfBytes = decoder.readUint32();
    var version = decoder.readUint32();
    val.microseconds = decoder.decodeStruct(codec.Int64);
    return val;
  };

  TimeDelta.encode = function(encoder, val) {
    var packed;
    encoder.writeUint32(TimeDelta.encodedSize);
    encoder.writeUint32(0);
    encoder.encodeStruct(codec.Int64, val.microseconds);
  };
  function TimeTicks(values) {
    this.initDefaults_();
    this.initFields_(values);
  }


  TimeTicks.prototype.initDefaults_ = function() {
    this.internalValue = 0;
  };
  TimeTicks.prototype.initFields_ = function(fields) {
    for(var field in fields) {
        if (this.hasOwnProperty(field))
          this[field] = fields[field];
    }
  };
  TimeTicks.generate = function(generator_) {
    var generated = new TimeTicks;
    generated.internalValue = generator_.generateInt64();
    return generated;
  };

  TimeTicks.prototype.mutate = function(mutator_) {
    if (mutator_.chooseMutateField()) {
      this.internalValue = mutator_.mutateInt64(this.internalValue);
    }
    return this;
  };
  TimeTicks.prototype.getHandleDeps = function() {
    var handles = [];
    return handles;
  };

  TimeTicks.prototype.setHandles = function() {
    this.setHandlesInternal_(arguments, 0);
  };
  TimeTicks.prototype.setHandlesInternal_ = function(handles, idx) {
    return idx;
  };

  TimeTicks.validate = function(messageValidator, offset) {
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


    return validator.validationError.NONE;
  };

  TimeTicks.encodedSize = codec.kStructHeaderSize + 8;

  TimeTicks.decode = function(decoder) {
    var packed;
    var val = new TimeTicks();
    var numberOfBytes = decoder.readUint32();
    var version = decoder.readUint32();
    val.internalValue = decoder.decodeStruct(codec.Int64);
    return val;
  };

  TimeTicks.encode = function(encoder, val) {
    var packed;
    encoder.writeUint32(TimeTicks.encodedSize);
    encoder.writeUint32(0);
    encoder.encodeStruct(codec.Int64, val.internalValue);
  };
  exports.Time = Time;
  exports.TimeDelta = TimeDelta;
  exports.TimeTicks = TimeTicks;
})();