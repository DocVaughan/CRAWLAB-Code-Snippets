################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
ASM_SRCS += \
..\src/reset_program.asm 

C_SRCS += \
..\src/SH2Tiny_Sample1.c \
..\src/hardware_setup.c \
..\src/interrupt_handlers.c \
..\src/vector_table.c 

C_DEPS += \
./src/SH2Tiny_Sample1.d \
./src/hardware_setup.d \
./src/interrupt_handlers.d \
./src/vector_table.d 

OBJS += \
./src/SH2Tiny_Sample1.o \
./src/hardware_setup.o \
./src/interrupt_handlers.o \
./src/reset_program.o \
./src/vector_table.o 

ASM_DEPS += \
./src/reset_program.d 


# Each subdirectory must supply rules for building sources it contributes
src/SH2Tiny_Sample1.o: ../src/SH2Tiny_Sample1.c
	@echo 'Scanning and building file: $<'
	@echo 'Invoking: Scanner and Compiler'
	@sh-elf-gcc -MM -MP -MF "src/SH2Tiny_Sample1.d" -MT"src/SH2Tiny_Sample1.o" -MT"src/SH2Tiny_Sample1.d" @"src/SH2Tiny_Sample1.depsub" "$<"
	@echo	sh-elf-gcc -MM -MP -MF "src/SH2Tiny_Sample1.d" -MT"src/SH2Tiny_Sample1.o" -MT"src/SH2Tiny_Sample1.d" -x c   -fomit-frame-pointer -DINIT_SECTIONS -D__BIG_ENDIAN__=1 -O2 -g -m2 -mb "$<"
	@sh-elf-gcc -Wa,-adlhn="$(basename $(notdir $<)).lst" @"src/SH2Tiny_Sample1.sub" -o "$(@:%.d=%.o)" "$<"
	@echo sh-elf-gcc -c -x c  -Wa,-adlhn="$(basename $(notdir $<)).lst" -fomit-frame-pointer -DINIT_SECTIONS -D__BIG_ENDIAN__=1 -O2 -g -m2 -mb -o "$(@:%.d=%.o)" "$<"
	@echo 'Finished scanning and building: $<'
	@echo.

src/hardware_setup.o: ../src/hardware_setup.c
	@echo 'Scanning and building file: $<'
	@echo 'Invoking: Scanner and Compiler'
	@sh-elf-gcc -MM -MP -MF "src/hardware_setup.d" -MT"src/hardware_setup.o" -MT"src/hardware_setup.d" @"src/hardware_setup.depsub" "$<"
	@echo	sh-elf-gcc -MM -MP -MF "src/hardware_setup.d" -MT"src/hardware_setup.o" -MT"src/hardware_setup.d" -x c   -fomit-frame-pointer -DINIT_SECTIONS -D__BIG_ENDIAN__=1 -O2 -g -m2 -mb "$<"
	@sh-elf-gcc -Wa,-adlhn="$(basename $(notdir $<)).lst" @"src/hardware_setup.sub" -o "$(@:%.d=%.o)" "$<"
	@echo sh-elf-gcc -c -x c  -Wa,-adlhn="$(basename $(notdir $<)).lst" -fomit-frame-pointer -DINIT_SECTIONS -D__BIG_ENDIAN__=1 -O2 -g -m2 -mb -o "$(@:%.d=%.o)" "$<"
	@echo 'Finished scanning and building: $<'
	@echo.

src/interrupt_handlers.o: ../src/interrupt_handlers.c
	@echo 'Scanning and building file: $<'
	@echo 'Invoking: Scanner and Compiler'
	@sh-elf-gcc -MM -MP -MF "src/interrupt_handlers.d" -MT"src/interrupt_handlers.o" -MT"src/interrupt_handlers.d" @"src/interrupt_handlers.depsub" "$<"
	@echo	sh-elf-gcc -MM -MP -MF "src/interrupt_handlers.d" -MT"src/interrupt_handlers.o" -MT"src/interrupt_handlers.d" -x c   -fomit-frame-pointer -DINIT_SECTIONS -D__BIG_ENDIAN__=1 -O2 -g -m2 -mb "$<"
	@sh-elf-gcc -Wa,-adlhn="$(basename $(notdir $<)).lst" @"src/interrupt_handlers.sub" -o "$(@:%.d=%.o)" "$<"
	@echo sh-elf-gcc -c -x c  -Wa,-adlhn="$(basename $(notdir $<)).lst" -fomit-frame-pointer -DINIT_SECTIONS -D__BIG_ENDIAN__=1 -O2 -g -m2 -mb -o "$(@:%.d=%.o)" "$<"
	@echo 'Finished scanning and building: $<'
	@echo.

src/reset_program.o: ../src/reset_program.asm
	@echo 'Scanning and building file: $<'
	@echo 'Invoking: Scanner and Compiler'
	@sh-elf-gcc -MM -MP -MF "src/reset_program.d" -MT"src/reset_program.o" -MT"src/reset_program.d" @"src/reset_program.depsub" "$<"
	@echo	sh-elf-gcc -MM -MP -MF "src/reset_program.d" -MT"src/reset_program.o" -MT"src/reset_program.d" -Wa,-gdwarf2 -x assembler-with-cpp   -fomit-frame-pointer -DINIT_SECTIONS -D__BIG_ENDIAN__=1 -O2 -g -m2 -mb "$<"
	@sh-elf-gcc -Wa,-adlhn="$(basename $(notdir $<)).lst" @"src/reset_program.sub" -o "$(@:%.d=%.o)" "$<"
	@echo sh-elf-gcc -Wa,-gdwarf2 -c -x assembler-with-cpp  -Wa,-adlhn="$(basename $(notdir $<)).lst" -fomit-frame-pointer -DINIT_SECTIONS -D__BIG_ENDIAN__=1 -O2 -g -m2 -mb -o "$(@:%.d=%.o)" "$<"
	@echo 'Finished scanning and building: $<'
	@echo.

src/vector_table.o: ../src/vector_table.c
	@echo 'Scanning and building file: $<'
	@echo 'Invoking: Scanner and Compiler'
	@sh-elf-gcc -MM -MP -MF "src/vector_table.d" -MT"src/vector_table.o" -MT"src/vector_table.d" @"src/vector_table.depsub" "$<"
	@echo	sh-elf-gcc -MM -MP -MF "src/vector_table.d" -MT"src/vector_table.o" -MT"src/vector_table.d" -x c   -fomit-frame-pointer -DINIT_SECTIONS -D__BIG_ENDIAN__=1 -O2 -g -m2 -mb "$<"
	@sh-elf-gcc -Wa,-adlhn="$(basename $(notdir $<)).lst" @"src/vector_table.sub" -o "$(@:%.d=%.o)" "$<"
	@echo sh-elf-gcc -c -x c  -Wa,-adlhn="$(basename $(notdir $<)).lst" -fomit-frame-pointer -DINIT_SECTIONS -D__BIG_ENDIAN__=1 -O2 -g -m2 -mb -o "$(@:%.d=%.o)" "$<"
	@echo 'Finished scanning and building: $<'
	@echo.

