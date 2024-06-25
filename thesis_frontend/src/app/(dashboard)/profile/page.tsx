import Breadcrumb from "@/components/Breadcrumbs/Breadcrumb";
import Image from "next/image";
import { Metadata } from "next";
import DefaultLayout from "@/components/Layouts/DefaultLayout";
import Link from "next/link";

export const metadata: Metadata = {
  title: "SM Admin",
  description: "",
};

const Profile = () => {
  return (
    <DefaultLayout>
      <div className="mx-auto max-w-242.5">
        <Breadcrumb pageName="Profile" />

        <div className="container mx-auto">
          <div className="flex flex-col md:flex-row">
            {/* Profile Nav */}
            <div className="w-full lg:w-2/5 mb-6 md:mb-0">
              <div className="overflow-hidden rounded-sm border border-stroke bg-white shadow-default dark:border-strokedark dark:bg-boxdark">
                <div className="relative z-20 h-35 md:h-30">
                  <Image
                    src={""}
                    alt="profile cover"
                    className="h-full w-full rounded-tl-sm rounded-tr-sm object-cover object-center"
                    width={970}
                    height={260}
                    style={{
                      width: "auto",
                      height: "auto",
                    }}
                  />
                  <div className="absolute bottom-1 right-1 z-10 xsm:bottom-4 xsm:right-4">
                    <label htmlFor="cover" className="">
                      <input
                        type="file"
                        name="cover"
                        id="cover"
                        className="sr-only"
                      />
                      <span>
                        <svg
                          className="fill-current"
                          width="14"
                          height="14"
                          viewBox="0 0 14 14"
                          fill="none"
                          xmlns="http://www.w3.org/2000/svg"
                        ></svg>
                      </span>
                    </label>
                  </div>
                </div>
                <div className="px-4 pb-6 text-center lg:pb-8 xl:pb-11.5">
                  <div className="relative z-30 mx-auto -mt-22 h-30 w-full max-w-30 rounded-full bg-white/20 p-1 backdrop-blur sm:h-44 sm:max-w-44 sm:p-3">
                    <div className="relative drop-shadow-2">
                      <Image
                        src={"/images/user/user-06.png"}
                        width={160}
                        height={160}
                        style={{
                          width: "auto",
                          height: "auto",
                        }}
                        alt="profile"
                      />
                      <label
                        htmlFor="profile"
                        className="absolute bottom-0 right-0 flex h-8.5 w-8.5 cursor-pointer items-center justify-center rounded-full bg-primary text-white hover:bg-opacity-90 sm:bottom-2 sm:right-2"
                      >
                        <svg
                          className="fill-current"
                          width="14"
                          height="14"
                          viewBox="0 0 14 14"
                          fill="none"
                          xmlns="http://www.w3.org/2000/svg"
                        >
                          <path
                            fillRule="evenodd"
                            clipRule="evenodd"
                            d="M4.76464 1.42638C4.87283 1.2641 5.05496 1.16663 5.25 1.16663H8.75C8.94504 1.16663 9.12717 1.2641 9.23536 1.42638L10.2289 2.91663H12.25C12.7141 2.91663 13.1592 3.101 13.4874 3.42919C13.8156 3.75738 14 4.2025 14 4.66663V11.0833C14 11.5474 13.8156 11.9925 13.4874 12.3207C13.1592 12.6489 12.7141 12.8333 12.25 12.8333H1.75C1.28587 12.8333 0.840752 12.6489 0.512563 12.3207C0.184375 11.9925 0 11.5474 0 11.0833V4.66663C0 4.2025 0.184374 3.75738 0.512563 3.42919C0.840752 3.101 1.28587 2.91663 1.75 2.91663H3.77114L4.76464 1.42638ZM5.56219 2.33329L4.5687 3.82353C4.46051 3.98582 4.27837 4.08329 4.08333 4.08329H1.75C1.59529 4.08329 1.44692 4.14475 1.33752 4.25415C1.22812 4.36354 1.16667 4.51192 1.16667 4.66663V11.0833C1.16667 11.238 1.22812 11.3864 1.33752 11.4958C1.44692 11.6052 1.59529 11.6666 1.75 11.6666H12.25C12.4047 11.6666 12.5531 11.6052 12.6625 11.4958C12.7719 11.3864 12.8333 11.238 12.8333 11.0833V4.66663C12.8333 4.51192 12.7719 4.36354 12.6625 4.25415C12.5531 4.14475 12.4047 4.08329 12.25 4.08329H9.91667C9.72163 4.08329 9.53949 3.98582 9.4313 3.82353L8.43781 2.33329H5.56219Z"
                            fill=""
                          />
                          <path
                            fillRule="evenodd"
                            clipRule="evenodd"
                            d="M7.00004 5.83329C6.03354 5.83329 5.25004 6.61679 5.25004 7.58329C5.25004 8.54979 6.03354 9.33329 7.00004 9.33329C7.96654 9.33329 8.75004 8.54979 8.75004 7.58329C8.75004 6.61679 7.96654 5.83329 7.00004 5.83329ZM4.08337 7.58329C4.08337 5.97246 5.38921 4.66663 7.00004 4.66663C8.61087 4.66663 9.91671 5.97246 9.91671 7.58329C9.91671 9.19412 8.61087 10.5 7.00004 10.5C5.38921 10.5 4.08337 9.19412 4.08337 7.58329Z"
                            fill=""
                          />
                        </svg>
                        <input
                          type="file"
                          name="profile"
                          id="profile"
                          className="sr-only"
                        />
                      </label>
                    </div>
                  </div>
                  <div className="flex items-center justify-center [&>div]:w-full mt-10">
                    <div
                      className=""
                      data-panel=""
                      data-panel-collapsible="true"
                      data-panel-id=":ra:"
                      data-panel-size={20.0}
                      id="data-panel-id-:ra:"
                      style={{ flex: "20 1 0px", overflow: "hidden" }}
                    >
                      <div className="flex h-[52px] items-center justify-center px-2">
                        <button
                          type="button"
                          role="combobox"
                          aria-controls="radix-:rb:"
                          aria-expanded="false"
                          aria-autocomplete="none"
                          dir="ltr"
                          data-state="closed"
                          className="h-9 w-full justify-between whitespace-nowrap rounded-md border border-input bg-transparent px-3 py-2 text-sm shadow-sm ring-offset-background placeholder:text-muted-foreground focus:outline-none focus:ring-1 focus:ring-ring disabled:cursor-not-allowed disabled:opacity-50 flex items-center gap-2 [&>span]:line-clamp-1 [&>span]:flex [&>span]:w-full [&>span]:items-center [&>span]:gap-1 [&>span]:truncate [&_svg]:h-4 [&_svg]:w-4 [&_svg]:shrink-0"
                          aria-label="Select account"
                        >
                          <span style={{ pointerEvents: "none" }}>
                            <svg
                              role="img"
                              viewBox="0 0 24 24"
                              xmlns="http://www.w3.org/2000/svg"
                            >
                              <title>Vercel</title>
                              <path
                                d="M24 22.525H0l12-21.05 12 21.05z"
                                fill="currentColor"
                              />
                            </svg>
                            <span className="ml-2">Alicia Koch</span>
                          </span>
                          <svg
                            width={15}
                            height={15}
                            viewBox="0 0 15 15"
                            fill="none"
                            xmlns="http://www.w3.org/2000/svg"
                            className="h-4 w-4 opacity-50"
                            aria-hidden="true"
                          >
                            <path
                              d="M4.93179 5.43179C4.75605 5.60753 4.75605 5.89245 4.93179 6.06819C5.10753 6.24392 5.39245 6.24392 5.56819 6.06819L7.49999 4.13638L9.43179 6.06819C9.60753 6.24392 9.89245 6.24392 10.0682 6.06819C10.2439 5.89245 10.2439 5.60753 10.0682 5.43179L7.81819 3.18179C7.73379 3.0974 7.61933 3.04999 7.49999 3.04999C7.38064 3.04999 7.26618 3.0974 7.18179 3.18179L4.93179 5.43179ZM10.0682 9.56819C10.2439 9.39245 10.2439 9.10753 10.0682 8.93179C9.89245 8.75606 9.60753 8.75606 9.43179 8.93179L7.49999 10.8636L5.56819 8.93179C5.39245 8.75606 5.10753 8.75606 4.93179 8.93179C4.75605 9.10753 4.75605 9.39245 4.93179 9.56819L7.18179 11.8182C7.35753 11.9939 7.64245 11.9939 7.81819 11.8182L10.0682 9.56819Z"
                              fill="currentColor"
                              fillRule="evenodd"
                              clipRule="evenodd"
                            />
                          </svg>
                        </button>
                      </div>
                      <div
                        data-orientation="horizontal"
                        role="none"
                        className="shrink-0 bg-border h-[1px] w-full"
                      />
                      <div
                        data-collapsed="false"
                        className="group flex flex-col gap-4 py-2 data-[collapsed=true]:py-2"
                      >
                        <nav className="grid gap-1 px-2 group-[[data-collapsed=true]]:justify-center group-[[data-collapsed=true]]:px-2">
                          <a
                            className="inline-flex items-center whitespace-nowrap text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 bg-primary text-primary-foreground hover:bg-primary/90 h-9 rounded-md px-3 dark:bg-muted dark:text-white dark:hover:bg-muted dark:hover:text-white justify-start"
                            href="#"
                          >
                            <svg
                              xmlns="http://www.w3.org/2000/svg"
                              width={24}
                              height={24}
                              viewBox="0 0 24 24"
                              fill="none"
                              stroke="currentColor"
                              strokeWidth={2}
                              strokeLinecap="round"
                              strokeLinejoin="round"
                              className="lucide lucide-inbox mr-2 h-4 w-4"
                            >
                              <polyline points="22 12 16 12 14 15 10 15 8 12 2 12" />
                              <path d="M5.45 5.11 2 12v6a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-6l-3.45-6.89A2 2 0 0 0 16.76 4H7.24a2 2 0 0 0-1.79 1.11z" />
                            </svg>
                            Inbox
                            <span className="ml-auto text-background dark:text-white">
                              128
                            </span>
                          </a>
                          <a
                            className="inline-flex items-center whitespace-nowrap text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 hover:bg-accent hover:text-accent-foreground h-9 rounded-md px-3 justify-start"
                            href="#"
                          >
                            <svg
                              xmlns="http://www.w3.org/2000/svg"
                              width={24}
                              height={24}
                              viewBox="0 0 24 24"
                              fill="none"
                              stroke="currentColor"
                              strokeWidth={2}
                              strokeLinecap="round"
                              strokeLinejoin="round"
                              className="lucide lucide-file mr-2 h-4 w-4"
                            >
                              <path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z" />
                              <path d="M14 2v4a2 2 0 0 0 2 2h4" />
                            </svg>
                            Drafts<span className="ml-auto">9</span>
                          </a>
                          <a
                            className="inline-flex items-center whitespace-nowrap text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 hover:bg-accent hover:text-accent-foreground h-9 rounded-md px-3 justify-start"
                            href="#"
                          >
                            <svg
                              xmlns="http://www.w3.org/2000/svg"
                              width={24}
                              height={24}
                              viewBox="0 0 24 24"
                              fill="none"
                              stroke="currentColor"
                              strokeWidth={2}
                              strokeLinecap="round"
                              strokeLinejoin="round"
                              className="lucide lucide-send mr-2 h-4 w-4"
                            >
                              <path d="m22 2-7 20-4-9-9-4Z" />
                              <path d="M22 2 11 13" />
                            </svg>
                            Sent
                          </a>
                          <a
                            className="inline-flex items-center whitespace-nowrap text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 hover:bg-accent hover:text-accent-foreground h-9 rounded-md px-3 justify-start"
                            href="#"
                          >
                            <svg
                              xmlns="http://www.w3.org/2000/svg"
                              width={24}
                              height={24}
                              viewBox="0 0 24 24"
                              fill="none"
                              stroke="currentColor"
                              strokeWidth={2}
                              strokeLinecap="round"
                              strokeLinejoin="round"
                              className="lucide lucide-archive-x mr-2 h-4 w-4"
                            >
                              <rect width={20} height={5} x={2} y={3} rx={1} />
                              <path d="M4 8v11a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8" />
                              <path d="m9.5 17 5-5" />
                              <path d="m9.5 12 5 5" />
                            </svg>
                            Junk<span className="ml-auto">23</span>
                          </a>
                          <a
                            className="inline-flex items-center whitespace-nowrap text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 hover:bg-accent hover:text-accent-foreground h-9 rounded-md px-3 justify-start"
                            href="#"
                          >
                            <svg
                              xmlns="http://www.w3.org/2000/svg"
                              width={24}
                              height={24}
                              viewBox="0 0 24 24"
                              fill="none"
                              stroke="currentColor"
                              strokeWidth={2}
                              strokeLinecap="round"
                              strokeLinejoin="round"
                              className="lucide lucide-trash2 mr-2 h-4 w-4"
                            >
                              <path d="M3 6h18" />
                              <path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6" />
                              <path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2" />
                              <line x1={10} x2={10} y1={11} y2={17} />
                              <line x1={14} x2={14} y1={11} y2={17} />
                            </svg>
                            Trash
                          </a>
                          <a
                            className="inline-flex items-center whitespace-nowrap text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 hover:bg-accent hover:text-accent-foreground h-9 rounded-md px-3 justify-start"
                            href="#"
                          >
                            <svg
                              xmlns="http://www.w3.org/2000/svg"
                              width={24}
                              height={24}
                              viewBox="0 0 24 24"
                              fill="none"
                              stroke="currentColor"
                              strokeWidth={2}
                              strokeLinecap="round"
                              strokeLinejoin="round"
                              className="lucide lucide-archive mr-2 h-4 w-4"
                            >
                              <rect width={20} height={5} x={2} y={3} rx={1} />
                              <path d="M4 8v11a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8" />
                              <path d="M10 12h4" />
                            </svg>
                            Archive
                          </a>
                        </nav>
                      </div>
                      <div
                        data-orientation="horizontal"
                        role="none"
                        className="shrink-0 bg-border h-[1px] w-full"
                      />
                      <div
                        data-collapsed="false"
                        className="group flex flex-col gap-4 py-2 data-[collapsed=true]:py-2"
                      ></div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {/* Profile Info */}
            <div className="w-full lg:w-4/5 md:pl-6">
              <div className="overflow-hidden rounded-sm border border-stroke bg-white shadow-default dark:border-strokedark dark:bg-boxdark"></div>
              <div className="bg-white shadow-md rounded-lg p-6 mb-6">
                <h2 className="text-2xl font-bold mb-4">Biographie</h2>
                <div className="grid grid-cols-2 gap-4">
                  <div className="text-sm">
                    <span className="font-bold">Prénom:</span> Camila
                  </div>
                  <div className="text-sm">
                    <span className="font-bold">Nom:</span> Smith
                  </div>
                  <div className="text-sm">
                    <span className="font-bold">Pays:</span> Australie
                  </div>
                  <div className="text-sm">
                    <span className="font-bold">Date de naissance:</span> 13
                    Juillet 1983
                  </div>
                  <div className="text-sm">
                    <span className="font-bold">Profession:</span> Designer UI
                  </div>
                  <div className="text-sm">
                    <span className="font-bold">Email:</span> jsmith@flatlab.com
                  </div>
                  <div className="text-sm">
                    <span className="font-bold">Mobile:</span> (12) 03 4567890
                  </div>
                  <div className="text-sm">
                    <span className="font-bold">Téléphone:</span> 88 (02) 123456
                  </div>
                </div>
              </div>

              <div className="grid md:grid-cols-2 gap-6">
                {/* Project Cards */}
                {[
                  {
                    title: "Envato Website",
                    color: "bg-red-500",
                    progress: 35,
                  },
                  {
                    title: "ThemeForest CMS",
                    color: "bg-teal-500",
                    progress: 63,
                  },
                  {
                    title: "VectorLab Portfolio",
                    color: "bg-green-500",
                    progress: 75,
                  },
                  {
                    title: "Adobe Muse Template",
                    color: "bg-purple-500",
                    progress: 50,
                  },
                ].map((project, index) => (
                  <div
                    key={index}
                    className="bg-white shadow-md rounded-lg p-6"
                  >
                    <div className="flex justify-between items-center mb-4">
                      <div
                        className={`w-16 h-16 rounded-full ${project.color} flex items-center justify-center text-white font-bold`}
                      >
                        {project.progress}%
                      </div>
                      <div>
                        <h3
                          className={`text-lg font-semibold ${project.color} text-white px-3 py-1 rounded`}
                        >
                          {project.title}
                        </h3>
                        <p className="text-sm text-gray-600 mt-2">
                          Début: 15 Juillet
                        </p>
                        <p className="text-sm text-gray-600">Fin: 15 Août</p>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    </DefaultLayout>
  );
};

export default Profile;
