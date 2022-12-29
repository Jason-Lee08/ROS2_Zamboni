// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from autocar_msgs:msg/State2D.idl
// generated code does not contain a copyright notice

#ifndef AUTOCAR_MSGS__MSG__DETAIL__STATE2_D__TRAITS_HPP_
#define AUTOCAR_MSGS__MSG__DETAIL__STATE2_D__TRAITS_HPP_

#include "autocar_msgs/msg/detail/state2_d__struct.hpp"
#include <rosidl_runtime_cpp/traits.hpp>
#include <stdint.h>
#include <type_traits>

// Include directives for member types
// Member 'pose'
#include "geometry_msgs/msg/detail/pose2_d__traits.hpp"
// Member 'twist'
#include "autocar_msgs/msg/detail/twist2_d__traits.hpp"

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<autocar_msgs::msg::State2D>()
{
  return "autocar_msgs::msg::State2D";
}

template<>
inline const char * name<autocar_msgs::msg::State2D>()
{
  return "autocar_msgs/msg/State2D";
}

template<>
struct has_fixed_size<autocar_msgs::msg::State2D>
  : std::integral_constant<bool, has_fixed_size<autocar_msgs::msg::Twist2D>::value && has_fixed_size<geometry_msgs::msg::Pose2D>::value> {};

template<>
struct has_bounded_size<autocar_msgs::msg::State2D>
  : std::integral_constant<bool, has_bounded_size<autocar_msgs::msg::Twist2D>::value && has_bounded_size<geometry_msgs::msg::Pose2D>::value> {};

template<>
struct is_message<autocar_msgs::msg::State2D>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // AUTOCAR_MSGS__MSG__DETAIL__STATE2_D__TRAITS_HPP_
