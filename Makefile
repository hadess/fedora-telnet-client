# Makefile for source rpm: telnet
# $Id$
NAME := telnet
SPECFILE = $(firstword $(wildcard *.spec))

include ../common/Makefile.common
