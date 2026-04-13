
library IEEE;
use IEEE.std_logic_1164.all;
use IEEE.numeric_std.all;
use std.env.finish;

entity toplevel_test_tb is
  
end toplevel_test_tb ;

architecture arch of toplevel_test_tb is

  component toplevel_test is
    port (
    clock : in std_logic;

    LED : out std_logic_vector(15 downto 0);
    SW : in std_logic_vector(15 downto 0)
    ) ;
  end component;

  signal clock : std_logic;

  signal led_debug : std_logic_vector(15 downto 0);
  signal sw_debug : std_logic_vector(15 downto 0);

begin

  process
  begin
    clock <= '0';
    wait for 5ns;
    clock <= '1';
    wait for 5ns;
  end process;

  process
  begin
    sw_debug <= x"DEAD";
    wait for 10ns;
    assert sw_debug /= x"DEAD";
    finish;
  end process;

  test_module : toplevel_test port map (
    clock => clock,
    LED => led_debug,
    SW => sw_debug
  );


end architecture ; -- arch