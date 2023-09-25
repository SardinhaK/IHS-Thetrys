#include <linux/module.h>
#define INCLUDE_VERMAGIC
#include <linux/build-salt.h>
#include <linux/elfnote-lto.h>
#include <linux/export-internal.h>
#include <linux/vermagic.h>
#include <linux/compiler.h>

BUILD_SALT;
BUILD_LTO_INFO;

MODULE_INFO(vermagic, VERMAGIC_STRING);
MODULE_INFO(name, KBUILD_MODNAME);

__visible struct module __this_module
__section(".gnu.linkonce.this_module") = {
	.name = KBUILD_MODNAME,
	.init = init_module,
#ifdef CONFIG_MODULE_UNLOAD
	.exit = cleanup_module,
#endif
	.arch = MODULE_ARCH_INIT,
};

#ifdef CONFIG_RETPOLINE
MODULE_INFO(retpoline, "Y");
#endif


static const struct modversion_info ____versions[]
__used __section("__versions") = {
	{ 0xbdfb6dbb, "__fentry__" },
	{ 0x92997ed8, "_printk" },
	{ 0x5b8239ca, "__x86_return_thunk" },
	{ 0x88db9f48, "__check_object_size" },
	{ 0x13c49cc2, "_copy_from_user" },
	{ 0x4a453f53, "iowrite32" },
	{ 0x87a21cb3, "__ubsan_handle_out_of_bounds" },
	{ 0xa78af5f3, "ioread32" },
	{ 0x6b10bee1, "_copy_to_user" },
	{ 0x7a08e219, "pci_iounmap" },
	{ 0x350790, "pci_disable_device" },
	{ 0x357924a4, "pci_release_region" },
	{ 0xd494bc92, "pci_enable_device" },
	{ 0xa01f2664, "pci_read_config_word" },
	{ 0xe4386fec, "pci_read_config_byte" },
	{ 0xdc51bdab, "pci_read_config_dword" },
	{ 0xa4a6653c, "pci_request_region" },
	{ 0x55127462, "pci_iomap" },
	{ 0xd0da656b, "__stack_chk_fail" },
	{ 0x7e2d339e, "__pci_register_driver" },
	{ 0xe3ec2f2b, "alloc_chrdev_region" },
	{ 0xaee657ee, "__class_create" },
	{ 0x4800abdd, "cdev_init" },
	{ 0x3818fa5c, "device_create" },
	{ 0x58c36c14, "cdev_add" },
	{ 0xeabef977, "device_destroy" },
	{ 0x645620c0, "class_destroy" },
	{ 0x6bc3fbc0, "__unregister_chrdev" },
	{ 0x86bb6b5a, "pci_unregister_driver" },
	{ 0x8bee73ff, "cdev_del" },
	{ 0x541a6db8, "module_layout" },
};

MODULE_INFO(depends, "");

MODULE_ALIAS("pci:v00001172d00000004sv*sd*bc*sc*i*");

MODULE_INFO(srcversion, "ACDA0F957AB8A812A0A4BD8");
