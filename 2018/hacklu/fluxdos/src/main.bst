(import $a from string)

(const %CONST 264)

(func $main

  (call $a)

  (push u16 65534)
  (push u16 1000)
  (sys :openfile)
  (push u16 1000)
  (push u16 0)
  (push u16 3)
  (sys :read)
  (push u16 3)
  (sys :close)

  (push u16 0)
  (store u16 200)
  (load u16 200)
  (push u16 %CONST)
  (while (!= i16)
    (push u16 65534)
    (push u16 1000)
    (sys :openfile)
    (store u16 500)

    (load u16 200)
    (push u16 8)
    (div u16)
    (load u8) ;; *[200] / 8
    (push u8 0)

    (load u16 200)
    (load u16 200)
    (push u16 3)
    (shr u16)
    (push u16 3)
    (shl u16)
    (sub u16)
    (shr u16)
    (push u16 1)
    (and u16) ;; c = *[0 + i / 8] >> (i % 8) & 1

    (push u16 2000)
    (load u16 500)
    (sys :read) ;; print '-> ', read(*[500], 2000, c)
    (load u16 500)
    (sys :close)

    (load u16 200)
    (push u16 1)
    (add u16)
    (store u16 200)
    (load u16 200)
    (push u16 %CONST)
    )

  )