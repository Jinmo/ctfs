volatile char mem[0x1000];
#define LD(x) mem[x]
int validate() {
        char R = 0, X, Y, Z, A, B, C, I, M, N, P, Q, O;
L0:
        goto L24;

L1:
        R = ~R;

L2:
        Z = 0x01;

L3:
        R += Z;

L4:
        R += Z;

L5:
        if(R == 0) goto L38;

L6:
        R += Z;

L7:
        // if(R == 0) goto L59;

L8:
        R += Z;

L9:
        // if(R == 0) goto L59;

L59:
L10:
        BUG();

L11:
        // goto L-1;

L12:
        X = 0x01;

L13:
        Y = 0x00;

L14:
        if(X == 0) goto L22;

L15:
        Z = X;

L16:
        Z &= B;

L17:
        if(Z == 0) goto L19;

L18:
        Y += A;

L19:
        X += X;

L20:
        A += A;

L21:
        goto L14;

L22:
        A = Y;

L23:
        goto L1;

L24:
        I = 0x00;

L25:
        M = 0x00;

L26:
        N = 0x01;

L27:
        P = 0x00;

L28:
        Q = 0x00;

L29:
        B = 0xe5;

L30:
        B += I;

L31:
        if(B == 0) goto L56;

L32:
        B = 0x80;

L33:
        B += I;

L34:
        A = LD(B);

L35:
        B = LD(I);

L36:
        R = 0x01;

L37:
        goto L12;

L38:
        O = M;

L39:
        O += N;

L40:
        M = N;

L41:
        N = O;

L42:
        A += M;

L43:
        B = 0x20;

L44:
        B += I;

L45:
        C = LD(B);

L46:
        A ^= C;

L47:
        P += A;

L48:
        B = 0x40;

L49:
        B += I;

L50:
        A = LD(B);

L51:
        A ^= P;

L52:
        Q |= A;

L53:
        A = 0x01;

L54:
        I += A;

L55:
        goto L29;

L56:
        if(Q == 0) return 0;
return 1;
}