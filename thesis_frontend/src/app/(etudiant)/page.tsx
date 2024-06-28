"use client"

import { useState, useRef } from "react"
import Image from 'next/image'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"

export default function ProfileSection() {
  const [profile, setProfile] = useState({
    firstName: "John",
    lastName: "Doe",
    email: "john.doe@example.com",
    studentId: "12345",
    profilePicture: null
  })

  const fileInputRef = useRef(null)

  const handleProfileChange = (e) => {
    setProfile({ ...profile, [e.target.name]: e.target.value })
  }

  const handleProfilePictureChange = (e) => {
    const file = e.target.files[0]
    if (file) {
      const reader = new FileReader()
      reader.onloadend = () => {
        setProfile({ ...profile, profilePicture: reader.result })
      }
      reader.readAsDataURL(file)
    }
  }

  const handleProfileSubmit = (e) => {
    e.preventDefault()
    console.log("Profile updated:", profile)
    // Implement API call to update profile
  }

  const triggerFileInput = () => {
    fileInputRef.current.click()
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Profil</CardTitle>
        <CardDescription>
          Gérez vos informations personnelles ici.
        </CardDescription>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleProfileSubmit} className="space-y-4">
          <div className="flex items-center space-x-4">
            <Avatar className="h-24 w-24">
              <AvatarImage src={profile.profilePicture} alt="Profile picture" />
              <AvatarFallback>{profile.firstName[0]}{profile.lastName[0]}</AvatarFallback>
            </Avatar>
            <div>
              <Button type="button" onClick={triggerFileInput}>
                Changer la photo
              </Button>
              <Input
                ref={fileInputRef}
                type="file"
                accept="image/*"
                className="hidden"
                onChange={handleProfilePictureChange}
              />
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-1">
              <Label htmlFor="firstName">Prénom</Label>
              <Input
                id="firstName"
                name="firstName"
                value={profile.firstName}
                onChange={handleProfileChange}
              />
            </div>
            <div className="space-y-1">
              <Label htmlFor="lastName">Nom</Label>
              <Input
                id="lastName"
                name="lastName"
                value={profile.lastName}
                onChange={handleProfileChange}
              />
            </div>
          </div>

          <div className="space-y-1">
            <Label htmlFor="email">Email</Label>
            <Input
              id="email"
              name="email"
              type="email"
              value={profile.email}
              onChange={handleProfileChange}
            />
          </div>

          <div className="space-y-1">
            <Label htmlFor="studentId">Numéro étudiant</Label>
            <Input
              id="studentId"
              name="studentId"
              value={profile.studentId}
              onChange={handleProfileChange}
            />
          </div>

          <Button type="submit">Mettre à jour le profil</Button>
        </form>
      </CardContent>
    </Card>
  )
}